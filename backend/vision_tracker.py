"""Hand tracking + gesture detection using MediaPipe Tasks API.

Compatible with mediapipe>=0.10.30 (Python 3.13 supported).
The legacy `mp.solutions.hands` API was removed in these versions,
so we use the newer `mediapipe.tasks.python.vision.HandLandmarker`.
"""
import math
import time
import urllib.request
from pathlib import Path
from typing import Any

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

from backend.config import (
    PINCH_THRESHOLD, PINCH_RELEASE, SWIPE_THRESHOLD,
    DEBOUNCE_MS, CAM_WIDTH, CAM_HEIGHT, CAM_FPS, CAM_INDEX,
    MODELS_DIR,
)
from backend.utils.filters import OneEuroFilter
from backend.utils.logger import get_logger

log = get_logger(__name__)

# ---------- Model download ----------
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/hand_landmarker.task"
)
MODEL_PATH = MODELS_DIR / "hand_landmarker.task"


def ensure_model() -> Path:
    """Download the hand_landmarker.task model if missing."""
    if MODEL_PATH.exists() and MODEL_PATH.stat().st_size > 1_000_000:
        return MODEL_PATH

    log.info("Downloading hand_landmarker.task ...")
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        log.info("Model saved to %s", MODEL_PATH)
    except Exception as e:
        log.error("Model download failed: %s", e)
        raise RuntimeError(
            "Failed to download hand_landmarker.task. "
            "Check internet or download manually from:\n" + MODEL_URL
        ) from e
    return MODEL_PATH


HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]


def draw_landmarks(frame: np.ndarray, landmarks: list) -> None:
    """Draw hand landmarks + connections on the frame (in-place)."""
    h, w = frame.shape[:2]
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, pts[a], pts[b], (0, 255, 180), 2)

    for (x, y) in pts:
        cv2.circle(frame, (x, y), 4, (0, 255, 255), -1)


class VisionTracker:
    """Detects hand gestures using MediaPipe Tasks HandLandmarker."""

    def __init__(self) -> None:
        model_path = ensure_model()

        base_options = mp_python.BaseOptions(model_asset_path=str(model_path))
        options = mp_vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=mp_vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        self.landmarker = mp_vision.HandLandmarker.create_from_options(options)

        self.gesture_state = "idle"
        self.prev_x: float | None = None
        self.swipe_accumulator = 0.0
        self.last_event_time = time.time()

        self.filter_x = OneEuroFilter()
        self.filter_y = OneEuroFilter()
        self.prev_time = time.time()
        self.frame_ts_ms = 0

    @staticmethod
    def _distance(p1: Any, p2: Any) -> float:
        return math.sqrt(
            (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2
        )

    def process_frame(self, frame: np.ndarray) -> tuple[dict, np.ndarray]:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        self.frame_ts_ms += 33
        result = self.landmarker.detect_for_video(mp_image, self.frame_ts_ms)

        packet: dict[str, Any] = {
            "x": 0.5, "y": 0.5, "z": 0.0,
            "gesture": "none",
            "scale": 1.0,
            "rotation": 0.0,
            "trigger": False,
        }

        if not result.hand_landmarks:
            self.gesture_state = "idle"
            self.prev_x = None
            self.swipe_accumulator = 0.0
            return packet, frame

        lm = result.hand_landmarks[0]
        now = time.time()
        dt = max(now - self.prev_time, 1e-3)
        self.prev_time = now

        draw_landmarks(frame, lm)

        palm_x = (lm[0].x + lm[5].x + lm[17].x) / 3.0
        palm_y = (lm[0].y + lm[5].y + lm[17].y) / 3.0
        smooth_x = self.filter_x(palm_x, dt)
        smooth_y = self.filter_y(palm_y, dt)
        packet["x"], packet["y"] = smooth_x, smooth_y

        extended = sum(
            1 for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]
            if lm[tip].y < lm[pip].y
        )
        if extended >= 4 and self.gesture_state == "idle":
            packet["trigger"] = True
            self.gesture_state = "tracking"

        pinch_dist = self._distance(lm[4], lm[8])
        if self.gesture_state != "pinch" and pinch_dist < PINCH_THRESHOLD:
            if (now - self.last_event_time) * 1000 > DEBOUNCE_MS:
                self.gesture_state = "pinch"
                packet["gesture"] = "pinch_start"
                self.last_event_time = now
        elif self.gesture_state == "pinch" and pinch_dist > PINCH_RELEASE:
            self.gesture_state = "tracking"
            packet["gesture"] = "pinch_end"
            self.last_event_time = now

        if self.gesture_state == "pinch":
            packet["scale"] = float(
                np.interp(pinch_dist, [0.02, 0.15], [0.4, 2.0])
            )
            packet["gesture"] = "pinch_active"

        if self.prev_x is not None and self.gesture_state == "tracking":
            dx = smooth_x - self.prev_x
            self.swipe_accumulator += dx
            if abs(self.swipe_accumulator) > SWIPE_THRESHOLD:
                direction = "right" if self.swipe_accumulator > 0 else "left"
                packet["gesture"] = f"swipe_{direction}"
                packet["rotation"] = float(self.swipe_accumulator * 5.0)
                self.swipe_accumulator = 0.0
                self.last_event_time = now

        if (now - self.last_event_time) > 0.8:
            self.swipe_accumulator *= 0.95

        self.prev_x = smooth_x

        cv2.putText(frame, f"Gesture: {packet['gesture']}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        return packet, frame

    def close(self) -> None:
        """Release MediaPipe resources."""
        try:
            self.landmarker.close()
        except Exception:
            pass


def open_camera() -> cv2.VideoCapture:
    """Open the webcam with the configured settings, with fallback."""
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        log.warning("Camera index %d failed; trying index 1", CAM_INDEX)
        cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        raise RuntimeError("No webcam available")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, CAM_FPS)
    return cap