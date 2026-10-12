#!/usr/bin/env bash
# Bootstrap script for Linux/macOS
set -e

echo "🔧 Setting up Vision AI Assistant..."

# Detect Python
PYTHON=${PYTHON:-python3}
if ! command -v "$PYTHON" &>/dev/null; then
    echo "❌ Python 3 not found. Install Python 3.11+ first."
    exit 1
fi

# Install PortAudio (needed by PyAudio)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew &>/dev/null; then
        brew install portaudio || true
    else
        echo "⚠️  Homebrew missing; install PortAudio manually if PyAudio fails."
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update && sudo apt-get install -y portaudio19-dev python3-pyaudio
fi

# Create venv
if [ ! -d "venv" ]; then
    "$PYTHON" -m venv venv
fi

# Activate + install
# shellcheck disable=SC1091
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete. Activate with: source venv/bin/activate"