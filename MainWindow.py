from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QPoint
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush

import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SNAKE!")
        # self.move(10, 10)
        self.display_width = 1600
        self.display_height = 900
        self.move(QApplication.desktop().screen().rect().center() - QPoint(self.display_width//2, self.display_height//2));

        self.label = QLabel(self)
        self.setCentralWidget(self.label)

        self.canvas = QImage(self.display_width, self.display_height, QImage.Format_RGBA8888)
        self.background = QImage(self.display_width, self.display_height, QImage.Format_RGBA8888)

        self.snake_width = 50
        self.objects = QImage(self.snake_width, self.snake_width, QImage.Format_RGBA8888)

        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update)
        self.timer.start(0) 

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.x1 = 0
        self.y1 = 0
        self.vel = 8

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape or e.key() == Qt.Key_Q:
            self.close()

        if e.key() == Qt.Key_Left or e.key() == Qt.Key_A:
            self.left = True
            self.right, self.up, self.down = False, False, False
        if e.key() == Qt.Key_Right or e.key() == Qt.Key_D:
            self.right = True
            self.left, self.up, self.down = False, False, False
        if e.key() == Qt.Key_Down or e.key() == Qt.Key_S:
            self.down = True
            self.right, self.up, self.left = False, False, False
        if e.key() == Qt.Key_Up or e.key() == Qt.Key_W:
            self.up = True
            self.right, self.left, self.down = False, False, False

    # def keyReleaseEvent(self, e):
        # if e.key() == Qt.Key_Left:
        #     self.left = False
        # if e.key() == Qt.Key_Right:
        #     self.right = False
        # if e.key() == Qt.Key_Down:
        #     self.down = False
        # if e.key() == Qt.Key_Up:
        #     self.up = False

    def random_color(self):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        a = 255
        r, g, b, a = hex(r)[2:], hex(g)[2:], hex(b)[2:], hex(a)[2:]
        if len(r) == 1:
            r = '0' + r
        if len(g) == 1:
            g = '0' + g
        if len(b) == 1:
            b = '0' + b
        if len(a) == 1:
            a = '0' + a
        hex_code =  '#' + r + g + b

        return hex_code

    def update(self):
        if self.left:
            self.x1 -= self.vel
        if self.right:
            self.x1 += self.vel
        if self.down:
            self.y1 += self.vel
        if self.up:
            self.y1 -= self.vel
        self.draw_something()

    def draw_something(self):
        n = 10
        w = self.display_width // n
        painter = QPainter(self.canvas)
        painter.fillRect(0, 0, self.display_width, self.display_height, Qt.white)

        painter_background = QPainter(self.background)
        painter_object = QPainter(self.objects)

        pen = QPen()
        pen.setWidth(3)
        brush = QBrush()
        # brush.setStyle(Qt.Dense1Pattern)
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(QtGui.QColor('red'))

        # ## Background
        # painter_background.setBrush(brush)
        # for i in range(n):
        #     for j in range(n):
        #         color = QtGui.QColor(self.random_color())
        #         # color.setAlphaF(random.random())
        #         brush.setColor(color)
        #         # color.setAlpha(255)
        #         painter_background.setBrush(brush)

        #         painter_background.drawRect(i*w, j*w, w, w)

        ## Object
        brush.setColor(QtGui.QColor('red'))
        # painter_object.fillRect(0, 0, self.display_width, self.display_height, Qt.white)
        painter_object.setBrush(brush)
        painter_object.drawRect(0, 0, self.snake_width, self.snake_width)

        ## Rendering
        painter.drawImage(0, 0, self.background)
        painter.drawImage(self.x1, self.y1, self.objects)
        self.label.setPixmap(QPixmap.fromImage(self.canvas))
        painter.end()
 