# Maintainer: enesehs <your-email@example.com>
pkgname=yt-dlp-gui-git
pkgver=1.0.0
pkgrel=1
pkgdesc="A modern Qt6 GUI for yt-dlp video downloader"
arch=('x86_64')
url="https://github.com/enesehs/yt-dlp-gui"
license=('MIT')
depends=('python' 'python-pyside6' 'yt-dlp' 'python-requests')
makedepends=('git')
provides=('yt-dlp-gui')
conflicts=('yt-dlp-gui')
source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
    cd "yt-dlp-gui"
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
    cd "yt-dlp-gui"
    
    install -dm755 "$pkgdir/opt/yt-dlp-gui"
    install -dm755 "$pkgdir/opt/yt-dlp-gui/src/ui"
    install -dm755 "$pkgdir/opt/yt-dlp-gui/src/logic"
    install -dm755 "$pkgdir/opt/yt-dlp-gui/assets/fonts"
    install -dm755 "$pkgdir/opt/yt-dlp-gui/assets/img"
    
    install -Dm755 main.py "$pkgdir/opt/yt-dlp-gui/main.py"
    install -Dm644 src/ui/main_window.py "$pkgdir/opt/yt-dlp-gui/src/ui/main_window.py"
    install -Dm644 src/ui/log_viewer.py "$pkgdir/opt/yt-dlp-gui/src/ui/log_viewer.py"
    install -Dm644 src/ui/style.qss "$pkgdir/opt/yt-dlp-gui/src/ui/style.qss"
    install -Dm644 src/logic/downloader.py "$pkgdir/opt/yt-dlp-gui/src/logic/downloader.py"
    
    touch "$pkgdir/opt/yt-dlp-gui/src/__init__.py"
    touch "$pkgdir/opt/yt-dlp-gui/src/ui/__init__.py"
    touch "$pkgdir/opt/yt-dlp-gui/src/logic/__init__.py"
    
    install -Dm644 assets/fonts/Mona-Sans.ttf "$pkgdir/opt/yt-dlp-gui/assets/fonts/Mona-Sans.ttf"
    install -Dm644 assets/img/logo.ico "$pkgdir/opt/yt-dlp-gui/assets/img/logo.ico"
    install -Dm644 assets/img/folder.svg "$pkgdir/opt/yt-dlp-gui/assets/img/folder.svg"
    
    install -Dm644 assets/img/logo.ico "$pkgdir/usr/share/pixmaps/yt-dlp-gui.png"
    
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/yt-dlp-gui" << 'EOF'
#!/bin/bash
cd /opt/yt-dlp-gui
exec python main.py "$@"
EOF
    chmod 755 "$pkgdir/usr/bin/yt-dlp-gui"
    
    install -Dm644 /dev/stdin "$pkgdir/usr/share/applications/yt-dlp-gui.desktop" << EOF
[Desktop Entry]
Type=Application
Name=yt-dlp-gui
Comment=A modern Qt6 GUI for yt-dlp video downloader
Exec=yt-dlp-gui
Icon=yt-dlp-gui
Categories=AudioVideo;Network;
Terminal=false
EOF
}
