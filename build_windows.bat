@echo off
setlocal enabledelayedexpansion

echo === Building yt-dlp-gui for Windows ===

if not exist .venv\Scripts\python.exe (
    echo ERROR: .venv not found. Run run.sh on Linux/macOS or create .venv on Windows first.
    exit /b 1
)

.venv\Scripts\python.exe -m pip install --upgrade pip >nul
.venv\Scripts\python.exe -m pip install -r requirements.txt >nul

if exist build rd /s /q build
if exist dist rd /s /q dist

.venv\Scripts\pyinstaller.exe --noconfirm --onefile --windowed --name "yt-dlp-gui" ^
    --icon "src/img/logo.ico" ^
    --add-data "src/ui/style.qss;src/ui" ^
    --add-data "assets/fonts/Mona-Sans.ttf;assets/fonts" ^
    --add-data "src/img/logo.ico;src/img" ^
    --add-data "src/img/folder.svg;src/img" ^
    --hidden-import "PySide6" ^
    main.py

if errorlevel 1 (
    echo ERROR: build failed.
    exit /b 1
)

echo === Done: dist\yt-dlp-gui.exe ===
