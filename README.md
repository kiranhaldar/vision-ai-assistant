# VISION — Real-Time Sci-Fi AI Assistant

A JARVIS-inspired AI assistant with **hand gesture control**, **voice interaction**,
and an **interactive 3D WebGL HUD** powered by Three.js.

## Architecture

    Backend (Python)              Frontend (Three.js)
    +------------------+          +------------------+
    | MediaPipe Hands  | <--WS--> | Particle 3D      |
    | OpenCV           |  :8765   | HUD Rings        |
    | SpeechRecognition|          | Telemetry        |
    | pyttsx3 TTS      |          | Voice Status     |
    +------------------+          +------------------+

## Quickstart

    # 1. Create virtual environment
    python -m venv venv
    .\venv\Scripts\Activate.ps1     # Windows
    # source venv/bin/activate      # Linux/macOS

    # 2. Install dependencies
    pip install -r requirements.txt

    # 3. Run backend
    python -m backend.app

    # 4. In a second terminal, serve the frontend
    cd frontend
    python -m http.server 8000

    # 5. Open http://localhost:8000 in Chrome

## Gestures

| Gesture                | Action                |
|------------------------|-----------------------|
| Open palm              | Launch HUD            |
| Pinch (thumb + index)  | Scale 3D model        |
| Horizontal swipe       | Rotate 3D model       |

## Voice Commands

- "Open workplace"  -> Launches browser
- "Open YouTube"    -> Opens YouTube
- "Close"           -> Shuts down the assistant

## Project Structure

    vision-ai-assistant/
    |-- backend/          Python: CV, voice, WebSocket server
    |-- frontend/         HTML/CSS/JS: Three.js HUD
    |-- models/           MediaPipe / future ML models
    |-- tests/            pytest suite
    |-- scripts/          Setup & run scripts
    |-- docs/             Architecture, gestures, commands
    |-- logs/             Runtime logs (gitignored)

## Docs

See `docs/` for architecture, gesture vocabulary, and troubleshooting.
