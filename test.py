# import time
#
# from PyQt5 import QtGui, Qt
# from PyQt5 import QtWidgets
# import pygame
# import sys
#
# from PyQt5.QtCore import QRect
# from PyQt5.QtGui import QPainter, QPixmap, QFont
# from PyQt5.QtWidgets import QPushButton
#
#
# class ImageWidget(QtWidgets.QWidget):
#     def __init__(self, surface, parent=None):
#         super(ImageWidget, self).__init__(parent)
#         w = surface.get_width()
#         h = surface.get_height()
#         self.data = surface.get_buffer().raw
#         self.image = QtGui.QImage(self.data, w, h, QtGui.QImage.Format_RGB32)
#
#     def paintEvent(self, event):
#         my_paint = QtGui.QPainter()
#         my_paint.begin(self)
#         my_paint.drawImage(0, 0, self.image)
#         my_paint.end()
#
# class CustomButton(QPushButton):
#     def __init__(self, top_image_path, bottom_image_path, text, parent=None):
#         super().__init__(parent)
#         self.top_image_path = top_image_path
#         self.bottom_image_path = bottom_image_path
#         self.text = text
#         self.setFixedSize(100, 200)  # Установите размер кнопки по вашему усмотрению
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#         painter.setRenderHint(QPainter.Antialiasing)
#
#         # Рисуем верхнюю часть
#         top_image = QPixmap(self.top_image_path)
#         top_rect = QRect(0, 0, self.width(), self.height())
#         painter.drawPixmap(top_rect, top_image)
#
#         # Рисуем нижнюю часть
#         bottom_image = QPixmap(self.bottom_image_path)
#         bottom_rect = QRect(0, self.height() // 2, self.width(), self.height() // 2)
#         painter.drawPixmap(bottom_rect, bottom_image)
#
#         # Рисуем текст в центре нижней части
#         # painter.setFont(QFont('Arial', 12))
#         # painter.setPen(Qt.black)
#         # text_rect = QRect(0, self.height() // 2, self.width(), self.height() // 2)
#         # painter.drawText(text_rect, Qt.AlignCenter, self.text)
#
#
# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, surface, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.setFixedSize(640, 480)
#         self.setCentralWidget(ImageWidget(surface))
#
#         # button = QPushButton("Запустить игру", self)
#         button = CustomButton("resources/menu/v_menu_item.png", "resources/icons/ability_icons/fireball.png", "Запустить игру", self)
#
#         button.setGeometry(100, 100, 100, 30)
#
#
# pygame.init()
# my_surface = pygame.Surface((640, 480))
# my_surface.fill((10, 20, 205, 176))
# pygame.draw.circle(my_surface, (10, 70, 27, 255), (76, 76), 76)
#
# app = QtWidgets.QApplication(sys.argv)
# my_window = MainWindow(my_surface)
# my_window.show()
# app.exec_()
