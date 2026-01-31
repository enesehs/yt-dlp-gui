@echo off
echo Building yt-dlp-gui for Windows...

REM Ensure pyinstaller is installed
pip install pyinstaller

REM Clean previous builds
rd /s /q build dist

REM Build with PyInstaller
pyinstaller --noconfirm --onefile --windowed --name "yt-dlp-gui" ^
    --icon "assets/img/logo.ico" ^
    --add-data "src/ui/style.qss;src/ui" ^
    --add-data "assets/fonts/Mona-Sans.ttf;assets/fonts" ^
    --add-data "assets/img/logo.ico;assets/img" ^
    --hidden-import "PySide6" ^
    main.py

echo Build complete! Executable is in dist\yt-dlp-gui.exe
pause
