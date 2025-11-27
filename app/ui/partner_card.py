from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from utils.discount import calculate_partner_discount
from models import delete_partner

def format_price(val):
    return f"{val:,.2f} ₽".replace(',', ' ').replace('.', ',')

class PartnerCard(QWidget):
    def __init__(self, partner, total_sales, sample_price, on_edit, on_history, on_delete, parent=None):
        super().__init__(parent)
        self.partner = partner
        self.total_sales = total_sales
        self.sample_price = sample_price
        self.on_edit = on_edit
        self.on_history = on_history
        self.on_delete = on_delete
        self.setObjectName("partner_card")
        self._build_ui()

    def _build_ui(self):
        main = QHBoxLayout()
        main.setContentsMargins(10, 10, 10, 10)

        # LEFT block
        left = QVBoxLayout()
        left.addWidget(QLabel(f"<b>{self.partner['partner_type']} | {self.partner['name']}</b>"))
        left.addWidget(QLabel(f"{self.partner.get('director_fullname','')}"))
        left.addWidget(QLabel(self.partner.get('phone','')))
        left.addWidget(QLabel(f"Рейтинг: {self.partner.get('rating',0)}"))
        left.addStretch()

        # RIGHT block
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignmentFlag.AlignRight)

        # discount & price
        discount_rate = calculate_partner_discount(self.total_sales)
        discount_pct = f"{int(discount_rate*100)}%"
        lbl_discount = QLabel(f"<b>{discount_pct}</b>")
        final_price = self.sample_price * (1 - discount_rate)
        lbl_price = QLabel(format_price(final_price))
        lbl_discount.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl_price.setAlignment(Qt.AlignmentFlag.AlignRight)

        # buttons row
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignRight)

        btn_history = QPushButton("История")
        btn_edit = QPushButton("✎")
        btn_edit.setFixedWidth(32)
        btn_edit.setObjectName("accent")

        btn_delete = QPushButton("✖")
        btn_delete.setFixedWidth(32)
        btn_delete.setStyleSheet("background-color:#E57373; color:white;")

        btn_history.clicked.connect(lambda: self.on_history(self.partner['id']))
        btn_edit.clicked.connect(lambda: self.on_edit(self.partner['id']))
        btn_delete.clicked.connect(lambda: self.on_delete(self.partner['id']))

        btn_row.addWidget(btn_history)
        btn_row.addWidget(btn_edit)
        btn_row.addWidget(btn_delete)

        right.addWidget(lbl_discount)
        right.addWidget(lbl_price)
        right.addStretch()
        right.addLayout(btn_row)

        # combine
        main.addLayout(left)
        main.addLayout(right)
        self.setLayout(main)
