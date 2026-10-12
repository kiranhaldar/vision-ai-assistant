"""Centralized configuration loaded from environment variables."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# --- WebSocket ---
WS_HOST = os.getenv("WS_HOST", "0.0.0.0")
WS_PORT = int(os.getenv("WS_PORT", "8765"))

# --- Camera ---
CAM_INDEX = int(os.getenv("CAM_INDEX", "0"))
CAM_WIDTH = int(os.getenv("CAM_WIDTH", "640"))
CAM_HEIGHT = int(os.getenv("CAM_HEIGHT", "480"))
CAM_FPS = int(os.getenv("CAM_FPS", "30"))

# --- Gesture thresholds ---
PINCH_THRESHOLD = float(os.getenv("PINCH_THRESHOLD", "0.045"))
PINCH_RELEASE = float(os.getenv("PINCH_RELEASE", "0.065"))
SWIPE_THRESHOLD = float(os.getenv("SWIPE_THRESHOLD", "0.12"))
DEBOUNCE_MS = int(os.getenv("DEBOUNCE_MS", "250"))

# --- Voice ---
VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "en-US")
VOICE_RATE = int(os.getenv("VOICE_RATE", "175"))

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = ROOT_DIR / os.getenv("LOG_FILE", "logs/vision.log")

# --- Paths ---
MODELS_DIR = ROOT_DIR / "models"
LOGS_DIR = ROOT_DIR / "logs"
FRONTEND_DIR = ROOT_DIR / "frontend"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)