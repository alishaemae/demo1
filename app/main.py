# app/main.py
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def run():
    app = QApplication(sys.argv)
    try:
        with open("styles.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception:
        pass
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
