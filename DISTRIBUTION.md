# Distribution Guide for yt-dlp-gui

This guide covers how to package the application for Windows, Linux (AppImage), and Arch Linux (AUR), and how to publish it on GitHub.

## 1. GitHub Publishing

1.  **Create a Repository**:
    *   Go to GitHub and create a new repository named `yt-dlp-gui`.
2.  **Initialize Git**:
    ```bash
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/yt-dlp-gui.git
    git push -u origin main
    ```
3.  **Releases**:
    *   Go to "Releases" -> "Draft a new release".
    *   Tag version (e.g., `v1.0.0`).
    *   Upload the built executables (exe, AppImage) here.

---

## 2. Windows Packaging (exe)

We use `pyinstaller` to create a standalone executable.

**Prerequisites**:
- Python 3.10+ installed on Windows.
- `pip install pyinstaller`

**Build Command**:
```bash
pyinstaller --noconfirm --onefile --windowed --name "yt-dlp-gui" ^
    --icon "assets/img/logo.ico" ^
    --add-data "src/ui/style.qss:src/ui" ^
    --add-data "assets/fonts/Mona-Sans.ttf:assets/fonts" ^
    --add-data "assets/img/logo.png:assets/img" ^
    --hidden-import "PySide6" ^
    main.py
```
*Note: On Linux/Mac use `:` separator for `--add-data`, on Windows use `;` (e.g. `src/ui/style.qss;src/ui`).*

---

## 3. Linux Packaging (AppImage)

We use `appimagetool` and `python-appimage` or a manual directory structure.

**Method A: Using `linuxdeploy` (Recommended)**

1.  **Build Directory**:
    ```bash
    mkdir -p AppDir/usr/bin
    mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps
    mkdir -p AppDir/usr/share/applications
    ```
2.  **Copy Files**:
    *   Compile code to a binary (using PyInstaller as below) and place in `AppDir/usr/bin/yt-dlp-gui`.
    *   Copy logo to `AppDir/usr/share/icons/hicolor/256x256/apps/yt-dlp-gui.png`.
    *   Create `yt-dlp-gui.desktop` in `AppDir/usr/share/applications`.
3.  **Run linuxdeploy**:
    ```bash
    ./linuxdeploy-x86_64.AppImage --appdir AppDir --output appimage
    ```

**PyInstaller Command for Linux**:
```bash
pyinstaller --noconfirm --onefile --windowed --name "yt-dlp-gui" \
    --icon "assets/img/logo.png" \
    --add-data "src/ui/style.qss:src/ui" \
    --add-data "assets/fonts/Mona-Sans.ttf:assets/fonts" \
    --add-data "assets/img/logo.png:assets/img" \
    main.py
```

---

## 4. Arch Linux (AUR)

You need to create a `PKGBUILD` file.

**PKGBUILD Template**:
```bash
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
  install -Dm644 "assets/img/logo.png" "$pkgdir/usr/share/pixmaps/yt-dlp-gui.png"
  # Install python files... (Ideally requires setup.py)
  # Or simply copy files if not using standard python packing
}
```

*Note: For interpreted Python apps on AUR, it's best to use `setuptools` (`setup.py`) to install cleanly into `/usr/lib/python...`.*
