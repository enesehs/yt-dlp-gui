#!/bin/bash
echo "Building yt-dlp-gui for Linux..."

# Ensure pyinstaller is installed
./venv/bin/pip install pyinstaller

# Clean previous builds
rm -rf build dist

# Build with PyInstaller
./venv/bin/pyinstaller --noconfirm --onefile --windowed --name "yt-dlp-gui" \
    --icon "assets/img/logo.png" \
    --add-data "src/ui/style.qss:src/ui" \
    --add-data "assets/fonts/Mona-Sans.ttf:assets/fonts" \
    --add-data "assets/img/logo.png:assets/img" \
    --hidden-import "PySide6" \
    main.py

echo "Build complete! Executable is in dist/yt-dlp-gui"
