# Bootstrap script for Windows
Write-Host "🔧 Setting up Vision AI Assistant..." -ForegroundColor Cyan

# Verify Python
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host "❌ Python not found. Install Python 3.11+ first." -ForegroundColor Red
    exit 1
}

# Create venv
if (-not (Test-Path "venv")) {
    python -m venv venv
}

# Activate
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
python -m pip install --upgrade pip

# PyAudio on Windows often needs pipwin prebuilt wheel
Write-Host "📦 Installing PyAudio (pipwin fallback)..." -ForegroundColor Yellow
try {
    pip install PyAudio==0.2.14
} catch {
    pip install pipwin
    pipwin install pyaudio
}

pip install -r requirements.txt

Write-Host "✅ Setup complete. Activate with: .\venv\Scripts\Activate.ps1" -ForegroundColor Green