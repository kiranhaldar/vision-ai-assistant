# Architecture

## High-Level Diagram

    ┌─────────────────────────┐         ┌─────────────────────────┐
    │    BACKEND (Python)     │         │   FRONTEND (Browser)    │
    │                         │         │                         │
    │  ┌───────────────────┐  │         │  ┌───────────────────┐  │
    │  │ VisionTracker     │  │         │  │ Three.js Scene    │  │
    │  │ (MediaPipe Hands) │  │         │  │ (Particle Human)  │  │
    │  └────────┬──────────┘  │         │  └────────┬──────────┘  │
    │           │             │         │           │             │
    │  ┌────────▼──────────┐  │  WS     │  ┌────────▼──────────┐  │
    │  │  data_queue       │──┼────────►│  │ websocket_client  │  │
    │  │  (thread-safe)    │  │ :8765   │  │ hud_controller    │  │
    │  └───────────────────┘  │         │  │ gestures          │  │
    │                         │         │  └───────────────────┘  │
    │  ┌───────────────────┐  │         │                         │
    │  │ VoiceEngine       │  │         │                         │
    │  │ (STT + TTS)       │  │         │                         │
    │  └────────┬──────────┘  │         │                         │
    │           │             │         │                         │
    │  ┌────────▼──────────┐  │         │                         │
    │  │ CommandRouter     │  │         │                         │
    │  │ (browser, apps)   │  │         │                         │
    │  └───────────────────┘  │         │                         │
    └─────────────────────────┘         └─────────────────────────┘

## Threading Model

| Thread            | Responsibility                           |
|-------------------|------------------------------------------|
| Main (asyncio)    | WebSocket server, broadcast loop         |
| Vision thread     | Webcam + MediaPipe + queue push          |
| TTS worker thread | pyttsx3 via subprocess                   |
| STT background    | `speech_recognition.listen_in_background`|

The `data_queue` bridges the vision thread and the asyncio event loop
using a non-blocking `put_nowait` / `get_nowait` pattern.