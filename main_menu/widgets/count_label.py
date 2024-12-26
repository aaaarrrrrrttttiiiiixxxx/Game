from typing import Optional

from PyQt5.QtWidgets import QLabel

from main_menu.widgets.image_label import ImageLabel


class CountLabel(ImageLabel):
    def __init__(self, count: Optional[int], text: str, *args):
        self.title = text
        super().__init__(self._construct_text(count), *args)
        self.setVisible(count is not None)

    def _construct_text(self, count):
        return self.title + f' {count}' if count is not None else ''

    def update_count(self, count):
        self.setVisible(count is not None)
        self.setText(self._construct_text(count))
