from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout


class CustomButton(QPushButton):
    def __init__(self, percent_h, percent_w, bottom_image_path, text, parent=None):
        super().__init__(parent)
        pixmap = QPixmap(bottom_image_path)
        icon = QIcon(pixmap)
        self.setIcon(icon)
        self.percent_h = percent_h
        self.percent_w = percent_w
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")

        # текст кнопки
        label = QLabel(text, self)
        label.setStyleSheet("QLabel {font-size: 20px; font-weight: bold;}")
        label.setAlignment(Qt.AlignCenter)
        label_layout = QVBoxLayout(self)
        label_layout.addStretch()
        label_layout.addWidget(label)
        label_layout.addStretch()

    def change_size(self, new_main_window_w: int, new_main_window_h: int):
        new_w, new_h = int(new_main_window_w * self.percent_w), int(new_main_window_h * self.percent_h)
        self.setIconSize(QSize(new_w, new_h))
        self.setFixedSize(new_w, new_h)
