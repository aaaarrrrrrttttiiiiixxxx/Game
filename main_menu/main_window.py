from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, \
    QSizePolicy, QSpacerItem

from game import Game
from main_menu.best_result_repository import BestResultRepository
from main_menu.widgets.count_label import CountLabel
from main_menu.widgets.image_button import ImageButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" ")
        self.best_result_repository = BestResultRepository()
        self.setGeometry(100, 100, 800, 600)
        self.resizable_widgets = []
        self.init_ui_components()
        self.position_ui_components()
        self.show()

    def init_ui_components(self):
        self.button = ImageButton(0.25, 0.25, 'resources/menu/h_menu_item.png', "Run game")

        self.button.clicked.connect(self.handler)
        self.best_result_label = CountLabel(self.best_result_repository.result, "Best result:", 0.25, 0.25,
                                            'resources/menu/h_menu_item.png', self)
        self.curr_result_label = CountLabel(None, "Current result:", 0.25, 0.25, 'resources/menu/h_menu_item.png', self)

    def position_ui_components(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.add_widget(main_layout, self.best_result_label)
        self.add_widget(main_layout, self.curr_result_label)
        self.add_widget(main_layout, self.button)

        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))


    def add_widget(self, layout, widget):
        widget_layout = QHBoxLayout()
        widget_layout.addStretch()
        widget_layout.addWidget(widget)
        widget_layout.addStretch()

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addLayout(widget_layout)

        self.resizable_widgets.append(widget)

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
        self.best_result_label.change_size(width, height)
        self.curr_result_label.change_size(width, height)
