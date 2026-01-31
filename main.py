import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    
    font_path = os.path.join(os.path.dirname(__file__), "assets", "fonts", "Mona-Sans.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            if font_families:
                print(f"Loaded font: {font_families[0]}")
    
    style_path = os.path.join(os.path.dirname(__file__), "src", "ui", "style.qss")
    if os.path.exists(style_path):
        with open(style_path, "r") as f:
            app.setStyleSheet(f.read())
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

