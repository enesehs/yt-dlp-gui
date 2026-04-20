#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR=".venv"
PYTHON_BIN="${VENV_DIR}/bin/python"
PIP_BIN="${VENV_DIR}/bin/pip"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "==> Creating virtual environment (.venv)"
    python3 -m venv "$VENV_DIR"
fi

echo "==> Installing dependencies"
"$PIP_BIN" install -U pip >/dev/null
"$PIP_BIN" install -r requirements.txt >/dev/null

echo "==> Starting yt-dlp-gui"
exec "$PYTHON_BIN" main.py
