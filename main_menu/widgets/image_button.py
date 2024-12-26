from typing import Optional

from PyQt5.QtWidgets import QPushButton

from main_menu.widgets.image_label import ImageLabel


class ImageButton(QPushButton):
    def __init__(self, percent_h, percent_w, image_path, text, parent=None):
        super().__init__(parent)
        self.percent_h = percent_h
        self.percent_w = percent_w
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")

        self.text_label = ImageLabel(text, percent_h, percent_w, image_path, self)

    def change_size(self, new_main_window_w: int, new_main_window_h: int):
        new_w, new_h = int(new_main_window_w * self.percent_w), int(new_main_window_h * self.percent_h)
        self.setFixedSize(new_w, new_h)
        self.text_label.change_size(new_main_window_w, new_main_window_h)

    def setText(self, text: Optional[str]):
        self.text_label.setText(text)
