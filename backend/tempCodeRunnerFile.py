"""Vision AI Assistant - Main entrypoint.

Orchestrates:
  - MediaPipe hand tracking (separate thread)
  - Voice engine (background listening)
  - WebSocket server (async, broadcast loop)
"""
import asyncio
import json
import queue
import threading

import cv2
import websockets

from backend.command_router import CommandRouter
from backend.config import WS_HOST, WS_PORT
from backend.utils.logger import get_logger
from backend.vision_tracker import VisionTracker, open_camera
from backend.voice_engine import VoiceEngine

log = get_logger(__name__)

connected_clients: set = set()
data_queue: queue.Queue = queue.Queue(maxsize=2)
loop: asyncio.AbstractEventLoop | None = None
voice: VoiceEngine | None = None
router = CommandRouter()


# --------------------------------------------------------------- voice glue
def handle_voice_command(text: str) -> None:
    response, matched = router.route(text)
    if not matched:
        return
    if voice:
        voice.speak(response)
    if loop:
        asyncio.run_coroutine_threadsafe(
            broadcast({"type": "voice_event", "text": response}), loop
        )


# --------------------------------------------------------------- websocket
async def broadcast(message: dict) -> None:
    if not connected_clients:
        return
    payload = json.dumps(message)
    await asyncio.gather(
        *[c.send(payload) for c in connected_clients],
        return_exceptions=True,
    )


async def ws_handler(websocket, path=None) -> None:
    connected_clients.add(websocket)
    log.info("Client connected. Total: %d", len(connected_clients))
    try:
        async for _ in websocket:
            pass
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        log.info("Client disconnected. Total: %d", len(connected_clients))


async def data_broadcaster() -> None:
    while True:
        try:
            packet = data_queue.get_nowait()
            await broadcast({"type": "hand_data", **packet})
        except queue.Empty:
            pass
        await asyncio.sleep(0.016)


# --------------------------------------------------------------- vision
def vision_loop() -> None:
    try:
        cap = open_camera()
    except RuntimeError as e:
        log.error("Camera unavailable: %s. Gesture control disabled.", e)
        return

    tracker = VisionTracker()
    log.info("Hand tracking started.")

    while True:
        ret, frame = cap.read()
        if not ret:
            log.warning("Frame capture failed; stopping.")
            break
        frame = cv2.flip(frame, 1)
        packet, annotated = tracker.process_frame(frame)

        try:
            data_queue.put_nowait(packet)
        except queue.Full:
            pass

        cv2.imshow("Vision - Hand Tracking (q to quit)", annotated)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()


# --------------------------------------------------------------- main
async def main() -> None:
    global loop, voice
    loop = asyncio.get_running_loop()

    voice = VoiceEngine(handle_voice_command)
    voice.start_listening()
    voice.speak("Good afternoon sir. Vision online. All systems running at optimal performance. What is the plan?")
    voice = None  # voice engine will run in background thread

    threading.Thread(target=vision_loop, daemon=True).start()

    async with websockets.serve(ws_handler, WS_HOST, WS_PORT):
        log.info("WebSocket server on ws://%s:%d", WS_HOST, WS_PORT)
        await data_broadcaster()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Shutting down.")