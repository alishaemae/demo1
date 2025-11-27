from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QFrame, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from models import fetch_partners, total_sales_quantity_for_partner, sample_min_product_price
from ui.partner_card import PartnerCard
from ui.edit_partner_window import EditPartnerWindow
from ui.history_window import HistoryWindow
from models import delete_partner
from PyQt6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Партнёры — Мастер пол")
        self.setFixedSize(900, 600)  # запрещаем растягивание окна
        try:
            self.setWindowIcon(QIcon("resources/icon.ico"))
        except Exception:
            pass
        self._build_ui()
        self.load_partners()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # HEADER
        header = QFrame()
        header.setObjectName("header")
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10,10,10,10)

        # Логотип слева
        logo_lbl = QLabel()
        pix = QPixmap("resources/logo.png")
        if not pix.isNull():
            logo_lbl.setPixmap(pix.scaledToHeight(50))
        header_layout.addWidget(logo_lbl)
        header_layout.addStretch()

        # Кнопка добавить партнёра справа
        btn_add = QPushButton("Добавить партнёра")
        btn_add.setObjectName("accent")
        btn_add.setFixedHeight(36)
        btn_add.setFixedWidth(160)
        btn_add.clicked.connect(self.add_partner)
        header_layout.addWidget(btn_add)

        header.setLayout(header_layout)
        main_layout.addWidget(header)

        # SCROLL AREA для партнёров
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QFrame()
        container.setObjectName("main_container")
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(10,10,10,10)
        self.container_layout.setSpacing(10)
        scroll.setWidget(container)

        main_layout.addWidget(scroll)

    def load_partners(self):
        # очистка
        for i in reversed(range(self.container_layout.count())):
            item = self.container_layout.itemAt(i).widget()
            if item:
                item.setParent(None)
        try:
            partners = fetch_partners()
            sample_price = sample_min_product_price()
            for p in partners:
                total = total_sales_quantity_for_partner(p['id'])
                card = PartnerCard(p, total, sample_price, self.open_edit, self.open_history, self.delete_partner_ui)
                card.setFixedHeight(120)
                self.container_layout.addWidget(card)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить партнёров:\n{e}")

    def add_partner(self):
        dlg = EditPartnerWindow(self)
        if dlg.exec():
            self.load_partners()

    def delete_partner_ui(self, partner_id):
        ask = QMessageBox.question(
            self, "Удалить?",
            "Вы уверены, что хотите удалить партнера?\nОн исчезнет из приложения, но останется в БД со статусом 'Удалён'."
        )
        if ask == QMessageBox.StandardButton.Yes:
            delete_partner(partner_id)
            self.load_partners()

    def open_edit(self, partner_id):
        dlg = EditPartnerWindow(self, partner_id)
        if dlg.exec():
            self.load_partners()

    def open_history(self, partner_id):
        dlg = HistoryWindow(partner_id, self)
        dlg.exec()
