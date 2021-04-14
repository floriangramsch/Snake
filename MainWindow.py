from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QPoint
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QLabel, QVBoxLayout, QApplication, QLineEdit, QDialog, QPushButton, QFormLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor

import random

from Snake import Snake
from Settings import Settings

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SNAKE!")
        self.window_width = 1600
        self.window_height = 900
        self.game_width = 900
        self.game_height = 900
        self.resize(self.window_width, self.window_height)
        self.move(QApplication.desktop().screen().rect().center() - QPoint(self.window_width/2, self.window_height/2));
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.label = QLabel()
        self.label.resize(self.game_width, self.game_height)
        self.label.setMaximumWidth(900)
        self.label.setStyleSheet("border: 5px solid black;")

        self.settings = Settings(self)
        # self.settings.sizePolicy(QSizePolicyExpanding)
        self.settings.setMaximumWidth(200)

        self.hbox = QHBoxLayout(self.centralWidget)
        self.hbox.addWidget(self.settings)
        self.hbox.addWidget(self.label)

        self.centralWidget.setLayout(self.hbox)
        self.initialize()

    def user_input(self):
        d = QDialog()
        d.setWindowTitle("Semester Information")

        # kann der Dialog umgangen werden um andere Fenster zu bedienen?
        d.setWindowModality(Qt.ApplicationModal) # nein (Standard)
        # d.setWindowModality(qc.Qt.WindowModal)    # ja

        # ... wie QWidget verwendbar
        fbox = QFormLayout()

        input_name = QLineEdit()
        fbox.addRow("Name:", input_name)

        btnok = QPushButton("Start the Game",d)
        btnno = QPushButton("Nee, lieber doch nicht!",d)
        fbox.addRow(btnok, btnno)

        d.setLayout(fbox)

        # akzeptieren / ablehnen
        btnok.clicked.connect(lambda: d.accept())
        btnno.clicked.connect(lambda: d.reject())

        # bei Fehler / Erfolg an Hauptfenster melden
        d.accepted.connect(lambda: self.close())
        d.rejected.connect(lambda: self.quit())

        # Extras
        btnok.setDefault(True)           # btn wird bei Enter gedrückt
        d.exec_()

    def initialize(self):
        self.user_input()

        self.canvas = QImage(self.game_width, self.game_height, QImage.Format_RGBA8888)
        # self.canvas.setStyleSheet("border: 5px solid black;")
        self.background = QImage(self.game_width, self.game_height, QImage.Format_RGBA8888)
        self.snake_ebene = QImage(self.game_width, self.game_height, QImage.Format_RGBA8888)

        self.timer = QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.update)
        self.timer.start(300)

        self.snake = Snake(0, 0)
        self.snake.width = self.game_width / self.settings.game_size.value()

        ## Painter & Brush
        self.painter_canvas = QPainter(self.canvas)
        self.painter_background = QPainter(self.background)
        self.painter_snake = QPainter(self.snake_ebene)
        
        self.brush = QBrush()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Q:
            self.close()

        if e.key() == Qt.Key_O:
            if self.settings.hidden:
                self.settings.show()
                self.settings.hidden = not self.settings.hidden
            else:
                self.settings.hide()
                self.settings.hidden = not self.settings.hidden


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
        self.snake.width = self.game_width / self.settings.game_size.value()
        # self.snake.vel = self.settings.vel.value() * self.snake.width
        # self.snake.vel = self.snake.width
        self.snake.vel = self.snake.width
        self.snake.move()
        if self.settings.border.isChecked():
            if self.snake.x < 0 or self.snake.x + self.snake.width > self.game_width or self.snake.y < 0 or self.snake.y + self.snake.width > self.game_width:
                self.snake.vel = 0
                self.snake.x = 0
                self.snake.y = 0
                self.snake.change_dir("Right")
                self.snake.right = False
                print("LOST!")
        else:
            if self.snake.x < 0:
                self.snake.x = self.game_width - self.snake.width
            if self.snake.x >= self.game_width:
                self.snake.x = 0

            if self.snake.y < 0:
                self.snake.y = self.game_width - self.snake.width
                pass
            if self.snake.y>= self.game_width:
                self.snake.y = 0
        self.timer.start(self.snake.width * self.settings.vel.value()) 
        self.render()

    def draw_canvas(self):
        self.painter_canvas.fillRect(0, 0, self.game_width, self.game_height, Qt.white)

    def draw_snake_ebene(self):
        self.snake_ebene.fill(Qt.transparent)
        self.brush.setStyle(Qt.SolidPattern)
        self.brush.setColor(QtGui.QColor('red'))
        self.painter_snake.setBrush(self.brush)
        # self.painter_snake.drawRect(self.snake.x, self.snake.y, self.snake.width, self.snake.width)
        self.painter_snake.drawRoundedRect(self.snake.x, self.snake.y, self.snake.width, self.snake.width, 2.0, 2.0)

        self.painter_canvas.drawImage(0, 0, self.snake_ebene)

    def draw_background(self):
        # self.brush.setStyle(Qt.Dense1Pattern)
        self.background.fill(Qt.transparent)
        w = self.game_width / self.settings.game_size.value()
        self.painter_background.setBrush(self.brush)

        color1 = QColor(Qt.green)
        color1.setAlpha(20)
        color2 = QColor(Qt.green)
        color2.setAlpha(100)
        for i in range(self.settings.game_size.value()):
            for j in range(self.settings.game_size.value()):
                # color = QColor(self.random_color())
                # color.setAlpha(random.choice([20, 100]))
                # color.setAlpha(random.randint(0, 255))
                if (i+j) % 2 == 0:
                    self.brush.setColor(color1)
                else:
                    self.brush.setColor(color2)
                # color.setAlpha(255)
                self.painter_background.setBrush(self.brush)
                self.painter_background.drawRect(i*w, j*w, w, w)
        
        self.painter_canvas.drawImage(0, 0, self.background)

    def render(self):
        self.draw_canvas()
        self.draw_background()
        self.draw_snake_ebene()

        self.label.setPixmap(QPixmap.fromImage(self.canvas))
        # self.painter_canvas.end()
 