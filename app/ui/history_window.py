from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame
from PyQt6.QtCore import Qt
from models import fetch_partner_history

class HistoryWindow(QDialog):
    def __init__(self, partner_id, parent=None):
        super().__init__(parent)
        self.partner_id = partner_id
        self.setWindowTitle("История партнёра")
        self.setFixedSize(500, 400)  
        self.init_ui()
        self.load_history()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QFrame()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setSpacing(8)
        scroll.setWidget(container)

        main_layout.addWidget(scroll)
        close_btn = QPushButton("Закрыть")
        close_btn.setStyleSheet("background-color: #67BA80; color: white;")
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)

    def load_history(self):
        try:
            history = fetch_partner_history(self.partner_id)
            if not history:
                self.container_layout.addWidget(QLabel("История отсутствует"))
            else:
                for item in history:
                    lbl = QLabel(f"{item['date']}: {item['action']}")
                    lbl.setWordWrap(True)
                    self.container_layout.addWidget(lbl)
        except Exception as e:
            self.container_layout.addWidget(QLabel(f"Ошибка загрузки истории: {e}"))
