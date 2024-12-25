from typing import Optional

from PyQt5.QtWidgets import QLabel


class CountLabel(QLabel):
    def __init__(self, text: str, count: Optional[int], *args):
        self.text = text
        super().__init__(self._construct_text(count), *args)

    def _construct_text(self, count):
        return self.text + f' {count}' if count is not None else ''

    def update_count(self, count):
        self.setText(self._construct_text(count))
