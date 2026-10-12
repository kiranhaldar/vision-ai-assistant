#!/usr/bin/env bash
# Launch the Vision backend with logging
set -e
cd "$(dirname "$0")/.."
source venv/bin/activate 2>/dev/null || true
python -m backend.app 2>&1 | tee -a logs/backend.log