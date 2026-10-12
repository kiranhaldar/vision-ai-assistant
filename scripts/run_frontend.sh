#!/usr/bin/env bash
# Serve the frontend on http://localhost:8000
cd "$(dirname "$0")/../frontend"
python -m http.server 8000