from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QPoint
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor

import random

from Snake import Snake

class SnakeGame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("border: 1px solid black;")
        # self.resize(1000, 1000)
        self.display_width = self.width()
        self.display_height = self.height()
        # self.setGeometry(0, 0, 1000, 1000)
        
        self.resize(1000, 1000)
        # self.display_width = 1000
        # self.display_height = 1000

        self.label = QLabel(self)
        self.initialize()


    def initialize(self):
        self.canvas = QImage(self.display_width, self.display_height, QImage.Format_RGBA8888)
        self.background = QImage(self.display_width, self.display_height, QImage.Format_RGBA8888)
        self.snake_ebene = QImage(self.display_width, self.display_height, QImage.Format_RGBA8888)

        self.timer = QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.update)
        self.timer.start(0) 

        self.snake = Snake(0, 0)

        ## Painter & Brush
        self.painter_canvas = QPainter(self.canvas)
        self.painter_background = QPainter(self.background)
        self.painter_snake = QPainter(self.snake_ebene)
        
        self.brush = QBrush()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()

        if e.key() == Qt.Key_Escape or e.key() == Qt.Key_P:
            if self.timer.isActive:
                self.timer.stop()
            else:
                self.timer.start(0)
            self.timer.isActive = not self.timer.isActive

        if e.key() == Qt.Key_Left or e.key() == Qt.Key_A:
            self.snake.change_dir("Left")
        if e.key() == Qt.Key_Right or e.key() == Qt.Key_D:
            self.snake.change_dir("Right")
        if e.key() == Qt.Key_Down or e.key() == Qt.Key_S:
            self.snake.change_dir("Down")
        if e.key() == Qt.Key_Up or e.key() == Qt.Key_W:
            self.snake.change_dir("Up")

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
        self.snake.move()
        self.render()

    def draw_canvas(self):
        self.painter_canvas.fillRect(0, 0, self.display_width, self.display_height, Qt.white)

    def draw_snake_ebene(self):
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor('green'))
        self.painter_snake.fillRect(0, 0, self.display_width, self.display_height, Qt.white)
        # self.painter_snake.fillRect(0, 0, self.display_width, self.display_height, Qt.transparent)
        self.painter_snake.setBrush(self.brush)
        self.painter_snake.drawRect(self.snake.x, self.snake.y, self.snake.width, self.snake.width)

        self.painter_canvas.drawImage(0, 0, self.snake_ebene)

    def draw_background(self):
        self.brush.setStyle(Qt.Dense1Pattern)
        n = 10
        w = self.display_width // n
        h = self.display_height // n
        self.painter_background.setBrush(self.brush)
        for i in range(n):
            for j in range(n):
                color = QColor(self.random_color())
                # color.setAlphaF(random.random())
                self.brush.setColor(color)
                # color.setAlpha(255)
                self.painter_background.setBrush(self.brush)

                self.painter_background.drawRect(i*w, j*h, w, h)
        
        self.painter_canvas.drawImage(0, 0, self.background)

    def render(self):
        self.draw_canvas()
        # self.draw_background()
        self.draw_snake_ebene()

        self.label.setPixmap(QPixmap.fromImage(self.canvas))
        # self.painter_canvas.end()
 