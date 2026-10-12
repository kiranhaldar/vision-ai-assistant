
### `docs/TROUBLESHOOTING.md`

```markdown
# Troubleshooting

## Webcam not detected
- Confirm no other app (Zoom, Teams) is using the camera.
- Set `CAM_INDEX=1` in `.env`.
- On Linux, ensure `/dev/video0` exists.

## PyAudio installation fails
- **Windows**: `pip install pipwin && pipwin install pyaudio`
- **macOS**: `brew install portaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`

## MediaPipe reports "no module named mp"
- Ensure Python 3.11 or 3.12 (3.13 is unsupported).
- Reinstall: `pip install --force-reinstall mediapipe==0.10.14`

## WebSocket won't connect
- Check backend is running on port 8765: `netstat -ano | findstr 8765`
- Frontend must be served over HTTP (not `file://`).
- Check browser console for CORS / mixed-content errors.

## pyttsx3 hangs on Linux
- Install `espeak`: `sudo apt-get install espeak`
- Or set `espeak.voice` in `pyttsx3.init()`.