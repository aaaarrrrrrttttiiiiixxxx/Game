from typing import Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class ImageLabel(QLabel):
    def __init__(self, text, percent_h, percent_w, image_path, parent=None):
        super().__init__(parent)
        self.percent_h = percent_h
        self.percent_w = percent_w
        self.image_path = image_path
        self.text = text

        # Настройка изображения
        self.pixmap = QPixmap(image_path)
        self.setPixmap(self.pixmap)
        self.setScaledContents(True)

        # Настройка текста
        self.text_label = QLabel(text, self)
        self.text_label.setStyleSheet("QLabel {font-size: 20px; font-weight: bold;}")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setGeometry(0, 0, self.width(), self.height())

        # Устанавливаем начальный размер
        self.setFixedSize(int(parent.width() * self.percent_w), int(parent.height() * self.percent_h))

    def change_size(self, new_main_window_w: int, new_main_window_h: int):
        new_w, new_h = int(new_main_window_w * self.percent_w), int(new_main_window_h * self.percent_h)
        self.setFixedSize(new_w, new_h)
        self.text_label.setGeometry(0, 0, new_w, new_h)

    def setText(self, text: Optional[str]):
        self.text_label.setText(text)
