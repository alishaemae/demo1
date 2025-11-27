from PyQt6.QtWidgets import QDialog, QLineEdit, QLabel, QComboBox, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
from models import insert_partner, fetch_partner_by_id, update_partner

class EditPartnerWindow(QDialog):
    def __init__(self, parent=None, partner_id=None):
        super().__init__(parent)
        self.partner_id = partner_id
        self.logo_path = None
        self.setWindowTitle("Добавить партнёра" if partner_id is None else "Редактирование партнёра")
        self.setFixedSize(400, 500)  
        self.init_ui()
        if partner_id:
            self.load_data()

    def init_ui(self):
        self.type_cb = QComboBox()
        self.type_cb.addItems(["ЗАО","ООО","ПАО","ОАО"])
        self.name_le = QLineEdit()
        self.director_le = QLineEdit()
        self.phone_le = QLineEdit()
        self.email_le = QLineEdit()
        self.address_le = QLineEdit()
        self.inn_le = QLineEdit()
        self.rating_sb = QSpinBox()
        self.rating_sb.setRange(0, 100)

        self.logo_btn = QPushButton("Выбрать логотип")
        self.logo_btn.setStyleSheet("background-color: #67BA80; color: white;")
        self.logo_btn.clicked.connect(self.select_logo)

        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet("background-color: #67BA80; color: white;")
        save_btn.clicked.connect(self.save)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.close)

        layout = QVBoxLayout()
        layout.setSpacing(6)
        layout.addWidget(QLabel("Тип партнёра"))
        layout.addWidget(self.type_cb)
        layout.addWidget(QLabel("Наименование"))
        layout.addWidget(self.name_le)
        layout.addWidget(QLabel("ФИО директора"))
        layout.addWidget(self.director_le)
        layout.addWidget(QLabel("Телефон"))
        layout.addWidget(self.phone_le)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.email_le)
        layout.addWidget(QLabel("Юридический адрес"))
        layout.addWidget(self.address_le)
        layout.addWidget(QLabel("ИНН"))
        layout.addWidget(self.inn_le)
        layout.addWidget(QLabel("Рейтинг"))
        layout.addWidget(self.rating_sb)
        layout.addWidget(self.logo_btn)

        btn_row = QHBoxLayout()
        btn_row.addWidget(save_btn)
        btn_row.addWidget(cancel_btn)
        layout.addLayout(btn_row)

        self.setLayout(layout)

    def select_logo(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите логотип", "", "Изображения (*.png *.jpg *.bmp)")
        if file_path:
            self.logo_path = file_path

    def load_data(self):
        p = fetch_partner_by_id(self.partner_id)
        if not p:
            QMessageBox.critical(self, "Ошибка", "Партнёр не найден")
            self.reject()
            return
        idx = self.type_cb.findText(p['partner_type'])
        if idx >= 0:
            self.type_cb.setCurrentIndex(idx)
        self.name_le.setText(p['name'] or '')
        self.director_le.setText(p['director_fullname'] or '')
        self.phone_le.setText(p['phone'] or '')
        self.email_le.setText(p['email'] or '')
        self.address_le.setText(p['legal_address'] or '')
        self.inn_le.setText(p['inn'] or '')
        self.rating_sb.setValue(p['rating'] or 0)
        self.logo_path = p.get('logo_path')

    def save(self):
        name = self.name_le.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка ввода", "Наименование обязательно")
            return
        data = {
            'partner_type': self.type_cb.currentText(),
            'name': name,
            'director_fullname': self.director_le.text().strip(),
            'email': self.email_le.text().strip(),
            'phone': self.phone_le.text().strip(),
            'legal_address': self.address_le.text().strip(),
            'inn': self.inn_le.text().strip(),
            'rating': self.rating_sb.value(),
            'logo_path': self.logo_path
        }
        try:
            if self.partner_id:
                update_partner(self.partner_id, data)
            else:
                insert_partner(data)
            QMessageBox.information(self, "Готово", "Данные сохранены")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", str(e))
