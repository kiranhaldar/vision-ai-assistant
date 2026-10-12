# Models Directory

This folder holds machine-learning model artifacts used by the Vision backend.

## Contents

| File                    | Purpose                                |
|-------------------------|----------------------------------------|
| `hand_landmarker.task`  | Optional: MediaPipe Tasks API model    |

## Notes

- Large binary models are **gitignored** (see `.gitignore`).
- Run `python scripts/download_models.py` to fetch them.
- MediaPipe `mp.solutions.hands` downloads its model automatically on first run.
  The `.task` file is only needed if you migrate to the newer **Tasks API**.