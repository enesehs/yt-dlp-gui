# Maintainer: Your Name <email@example.com>
pkgname=yt-dlp-gui-git
pkgver=1.0.0
pkgrel=1
pkgdesc="A modern GUI for yt-dlp"
arch=('x86_64')
url="https://github.com/YOUR_USERNAME/yt-dlp-gui"
license=('MIT')
depends=('python-pyside6' 'yt-dlp' 'python-requests')
makedepends=('git' 'python-setuptools')
source=("git+$url.git")
md5sums=('SKIP')

pkgver() {
  cd "$pkgname"
  git describe --long --tags | sed 's/\([^-]*-g\)/r\1/;s/-/./g'
}

package() {
  cd "$pkgname"
  # This is a template. Adjust depending on how you structure your python install.
  # For simple scripts, you might just copy files.
  install -Dm644 "assets/img/logo.png" "$pkgdir/usr/share/pixmaps/yt-dlp-gui.png"
  install -Dm755 "main.py" "$pkgdir/usr/bin/yt-dlp-gui" 
}
