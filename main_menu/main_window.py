from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, \
    QSizePolicy, QSpacerItem

from config import WIDTH, HEIGHT
from game import Game
from main_menu.best_result_repository import BestResultRepository
from main_menu.widgets.count_label import CountLabel
from main_menu.widgets.image_button import CustomButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.best_result_repository = BestResultRepository()
        self.setGeometry(500, 500, WIDTH, HEIGHT)
        self.init_ui_components()
        self.position_ui_components()
        self.show()

    def init_ui_components(self):
        self.button = CustomButton(0.25, 0.2, 'resources/menu/h_menu_item.png', "Run game")

        self.button.clicked.connect(self.handler)
        self.best_result_label = CountLabel("Best result:", self.best_result_repository.result)
        self.curr_result_label = CountLabel("Current result:", None)

    def position_ui_components(self):
        self.setGeometry(100, 100, 800, 600)  # Устанавливаем начальный размер окна

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        h_layout_label1 = QHBoxLayout()
        h_layout_label1.addStretch()
        h_layout_label1.addWidget(self.best_result_label)
        h_layout_label1.addStretch()

        h_layout_label2 = QHBoxLayout()
        h_layout_label2.addStretch()
        h_layout_label2.addWidget(self.curr_result_label)
        h_layout_label2.addStretch()

        h_layout_button = QHBoxLayout()
        h_layout_button.addStretch()
        h_layout_button.addWidget(self.button)
        h_layout_button.addStretch()

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(h_layout_label1)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(h_layout_label2)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        main_layout.addLayout(h_layout_button)
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def handler(self):
        self.setVisible(False)
        my_game = Game()
        lvl = my_game.run()
        self.best_result_repository.save_result(lvl)
        self.curr_result_label.update_count(lvl)
        self.best_result_label.update_count(self.best_result_repository.result)
        self.setVisible(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Устанавливаем размеры кнопки в процентах от размера окна
        width = self.width()
        height = self.height()
        self.button.change_size(width, height)
