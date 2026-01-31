
pkgname=yt-dlp-gui-git
pkgver=r3.ec03f8c
pkgrel=1
pkgdesc="A modern Qt6 GUI for yt-dlp video downloader"
arch=('x86_64')
url="https://github.com/enesehs/yt-dlp-gui"
license=('MIT')

depends=(
  'python'
  'pyside6'
  'python-requests'
  'yt-dlp'
)

makedepends=('git')

provides=('yt-dlp-gui')
conflicts=('yt-dlp-gui')

source=("git+${url}.git")
sha256sums=('SKIP')

pkgver() {
  cd yt-dlp-gui
  printf "r%s.%s" \
    "$(git rev-list --count HEAD)" \
    "$(git rev-parse --short HEAD)"
}

package() {
  cd yt-dlp-gui

  install -dm755 "$pkgdir/usr/share/yt-dlp-gui"

  cp -r src assets main.py "$pkgdir/usr/share/yt-dlp-gui"

  chmod +x "$pkgdir/usr/share/yt-dlp-gui/main.py"

  install -Dm755 /dev/stdin "$pkgdir/usr/bin/yt-dlp-gui" <<'EOF'
exec python /usr/share/yt-dlp-gui/main.py "$@"
EOF

  install -Dm644 /dev/stdin \
    "$pkgdir/usr/share/applications/yt-dlp-gui.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=yt-dlp-gui
Comment=A modern Qt6 GUI for yt-dlp video downloader
Exec=yt-dlp-gui
Icon=yt-dlp-gui
Categories=AudioVideo;Network;
Terminal=false
EOF

  install -Dm644 assets/img/logo.ico \
    "$pkgdir/usr/share/pixmaps/yt-dlp-gui.ico"
}
