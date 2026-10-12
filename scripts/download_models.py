"""Download optional ML model artifacts into models/.

Currently a no-op placeholder. MediaPipe Solutions auto-downloads its
hand model on first use. Extend this script if you migrate to the
MediaPipe Tasks API or add Whisper / YOLO models.
"""
import urllib.request
from pathlib import Path

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

MODELS = {
    # Example (uncomment when ready to use Tasks API):
    # "hand_landmarker.task":
    #   "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
    #   "hand_landmarker/float16/1/hand_landmarker.task",
}


def download(name: str, url: str) -> None:
    dest = MODELS_DIR / name
    if dest.exists():
        print(f"✓ {name} already present")
        return
    print(f"↓ Downloading {name}...")
    urllib.request.urlretrieve(url, dest)
    print(f"✓ {name} saved")


def main() -> None:
    if not MODELS:
        print("No models configured. MediaPipe Solutions handles this automatically.")
        return
    for name, url in MODELS.items():
        download(name, url)


if __name__ == "__main__":
    main()