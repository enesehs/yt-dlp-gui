#!/usr/bin/env bash
set -euo pipefail

APP_NAME="yt-dlp-gui"
APP_DIR="AppDir"
PYTHON_BIN=".venv/bin/python"
PIP_BIN=".venv/bin/pip"
PYINSTALLER_BIN=".venv/bin/pyinstaller"
APPIMAGE_TOOL="appimagetool-x86_64.AppImage"

echo "==> Building ${APP_NAME} AppImage"

if [ ! -x "$PYTHON_BIN" ]; then
    echo "ERROR: .venv not found. Run ./run.sh once or create .venv first."
    exit 1
fi

"$PIP_BIN" install -U pip >/dev/null
"$PIP_BIN" install -r requirements.txt >/dev/null

rm -rf build dist "$APP_DIR" ./*.AppImage

"$PYINSTALLER_BIN" \
    --noconfirm \
    --onedir \
    --windowed \
    --name "$APP_NAME" \
    --icon "src/img/logo.ico" \
    --add-data "src/ui/style.qss:src/ui" \
    --add-data "assets/fonts/Mona-Sans.ttf:assets/fonts" \
    --add-data "src/img/logo.ico:src/img" \
    --add-data "src/img/folder.svg:src/img" \
    --hidden-import "PySide6" \
    main.py

mkdir -p "$APP_DIR/usr/bin"
mkdir -p "$APP_DIR/usr/share/applications"
mkdir -p "$APP_DIR/usr/share/icons/hicolor/256x256/apps"

cp -a "dist/${APP_NAME}/." "$APP_DIR/usr/bin/"

cat > "$APP_DIR/usr/share/applications/${APP_NAME}.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=yt-dlp-gui
Comment=GUI frontend for yt-dlp
Exec=${APP_NAME}
Icon=${APP_NAME}
Categories=AudioVideo;Network;
Terminal=false
StartupNotify=true
EOF

cp "$APP_DIR/usr/share/applications/${APP_NAME}.desktop" "$APP_DIR/${APP_NAME}.desktop"
cp "src/img/logo.ico" "$APP_DIR/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png"
cp "src/img/logo.ico" "$APP_DIR/${APP_NAME}.png"

cat > "$APP_DIR/AppRun" <<'EOF'
#!/usr/bin/env bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
exec "${HERE}/usr/bin/yt-dlp-gui" "$@"
EOF
chmod +x "$APP_DIR/AppRun"

if [ ! -f "$APPIMAGE_TOOL" ]; then
    echo "==> Downloading appimagetool"
    if command -v wget >/dev/null 2>&1; then
        wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/${APPIMAGE_TOOL}"
    elif command -v curl >/dev/null 2>&1; then
        curl -fsSL -o "$APPIMAGE_TOOL" "https://github.com/AppImage/AppImageKit/releases/download/continuous/${APPIMAGE_TOOL}"
    else
        echo "ERROR: wget or curl is required to download appimagetool"
        exit 1
    fi
    chmod +x "$APPIMAGE_TOOL"
fi

ARCH=x86_64 ./$APPIMAGE_TOOL "$APP_DIR" "${APP_NAME}-x86_64.AppImage"

echo "==> Done: ${APP_NAME}-x86_64.AppImage"
