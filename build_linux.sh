#!/bin/bash
echo "Building yt-dlp-gui AppImage for Linux..."

APP_NAME="yt-dlp-gui"
APP_DIR="AppDir"

./venv/bin/pip install pyinstaller

rm -rf build dist ${APP_DIR} *.AppImage

./venv/bin/pyinstaller --noconfirm --onedir --windowed --name "${APP_NAME}" \
    --add-data "src/ui/style.qss:src/ui" \
    --add-data "assets/fonts/Mona-Sans.ttf:assets/fonts" \
    --add-data "assets/img/logo.ico:assets/img" \
    --add-data "assets/img/folder.svg:assets/img" \
    --hidden-import "PySide6" \
    main.py

mkdir -p ${APP_DIR}/usr/bin
mkdir -p ${APP_DIR}/usr/share/applications
mkdir -p ${APP_DIR}/usr/share/icons/hicolor/256x256/apps

cp -r dist/${APP_NAME}/* ${APP_DIR}/usr/bin/

cat > ${APP_DIR}/usr/share/applications/${APP_NAME}.desktop << EOF
[Desktop Entry]
Type=Application
Name=yt-dlp-gui
Comment=Video downloader GUI for yt-dlp
Exec=${APP_NAME}
Icon=${APP_NAME}
Categories=AudioVideo;Network;
Terminal=false
EOF

cp ${APP_DIR}/usr/share/applications/${APP_NAME}.desktop ${APP_DIR}/

cp assets/img/logo.ico ${APP_DIR}/usr/share/icons/hicolor/256x256/apps/${APP_NAME}.png
cp assets/img/logo.ico ${APP_DIR}/${APP_NAME}.png

cat > ${APP_DIR}/AppRun << 'EOF'
#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
exec "${HERE}/usr/bin/yt-dlp-gui" "$@"
EOF
chmod +x ${APP_DIR}/AppRun

if [ ! -f appimagetool-x86_64.AppImage ]; then
    echo "Downloading appimagetool..."
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

ARCH=x86_64 ./appimagetool-x86_64.AppImage ${APP_DIR} ${APP_NAME}-x86_64.AppImage

echo "Build complete! AppImage: ${APP_NAME}-x86_64.AppImage"
