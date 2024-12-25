from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel

from config import WIDTH, HEIGHT
from game import Game
from main_menu.best_result_repository import BestResultRepository
from main_menu.widgets.count_label import CountLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.best_result_repository = BestResultRepository()
        self.setGeometry(500, 500, WIDTH, HEIGHT)
        self.ui_components()
        self.show()

    def ui_components(self):
        self.button = QPushButton("Run game", self)
        self.button.setGeometry((WIDTH - 100) // 2, (HEIGHT - 30) // 2, 100, 30)

        self.best_result_label = CountLabel("Best result:", self.best_result_repository.result, self)
        self.curr_result_label = CountLabel("Current result:", None, self)
        self.button.clicked.connect(self.handler)

    def handler(self):
        self.setVisible(False)
        my_game = Game()
        lvl = my_game.run()
        self.best_result_repository.save_result(lvl)
        self.curr_result_label.update_count(lvl)
        self.best_result_label.update_count(self.best_result_repository.result)
        self.setVisible(True)

