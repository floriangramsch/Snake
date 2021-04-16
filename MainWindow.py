from PyQt5 import QtGui
from PyQt5.QtCore import QRect, Qt, QTimer, QPoint
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QWidget, QLabel, QVBoxLayout, QApplication, QLineEdit, QDialog, QPushButton, QFormLayout, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor

import random

from Snake import Snake
from Settings import Settings
from Fruit import Fruit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SNAKE!")
        self.window_width = 1600
        self.window_height = 900
        self.game_width = 900
        self.game_height = 900
        self.resize(self.window_width, self.window_height)

        # Center the window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.label = QLabel()
        self.label.resize(self.game_width, self.game_height)
        self.label.setMaximumWidth(900)
        self.label.setStyleSheet("border: 5px solid black;")

        self.settings = Settings(self)
        self.settings.setMaximumWidth(200)

        self.hbox = QHBoxLayout(self.centralWidget)
        self.hbox.addWidget(self.settings)
        self.hbox.addWidget(self.label)

        self.centralWidget.setLayout(self.hbox)
        self.initialize()

    def user_input(self):
        d = QDialog()
        d.setWindowTitle("Settings")

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
        # self.settings.hide()

        tile_width = self.game_width / self.settings.game_size.value()
        self.snake = Snake(0, 0, tile_width)

        self.fruit = Fruit(56.25, 56.25, tile_width)
        self.fruit.new_position(self.game_width, self.settings.game_size.value())

        self.canvas = QImage(self.game_width, self.game_height, QImage.Format_RGBA8888)
        # self.canvas.setStyleSheet("border: 5px solid black;")
        self.background = QImage(self.game_width, self.game_height, QImage.Format_RGBA8888)
        self.snake_ebene = QImage(self.game_width, self.game_height, QImage.Format_RGBA8888)
        self.fruit_ebene = QImage(tile_width, tile_width, QImage.Format_RGBA8888)

        self.timer = QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.update)
        self.timer.start(300)


        ## Painter & Brush
        self.painter_canvas = QPainter(self.canvas)
        self.painter_background = QPainter(self.background)
        self.painter_snake = QPainter(self.snake_ebene)
        self.painter_fruit = QPainter(self.fruit_ebene)
        
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
            self.snake.change_dir([-1, 0])
        if e.key() == Qt.Key_Right or e.key() == Qt.Key_D:
            self.snake.change_dir([1, 0])
        if e.key() == Qt.Key_Down or e.key() == Qt.Key_S:
            self.snake.change_dir([0, 1])
        if e.key() == Qt.Key_Up or e.key() == Qt.Key_W:
            self.snake.change_dir([0, -1])


        if e.key() == Qt.Key_E:
            self.snake.add_length()

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
        self.snake.vel = self.snake.width

        self.snake.move(self.game_width, self.settings.border.isChecked())

        self.settings.snake_x.setText(str(self.snake.body[0][0]))
        self.settings.snake_y.setText(str(self.snake.body[0][1]))
        self.settings.fruit_x.setText(str(self.fruit.pos[0]))
        self.settings.fruit_y.setText(str(self.fruit.pos[1]))

        if self.snake.body[0] == self.fruit.pos:
            self.fruit.new_position(self.game_width, self.settings.game_size.value())
            self.snake.add_length()

        self.timer.start(self.snake.width * self.settings.vel.value()) 
        self.render()

    def draw_canvas(self):
        self.painter_canvas.fillRect(0, 0, self.game_width, self.game_height, Qt.white)

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
                # # color = QColor(self.random_color())
                # # color1.setAlpha(random.choice([20, 100]))
                # color1.setAlpha(random.randint(0, 255))
                # self.brush.setColor(color1)
                if (i+j) % 2 == 0:
                    self.brush.setColor(color1)
                else:
                    self.brush.setColor(color2)
                self.painter_background.setBrush(self.brush)
                self.painter_background.drawRect(i*w, j*w, w, w)
        
    def died(self):
        self.snake.revive()
        d = QDialog()
        d.setWindowTitle("Looser..")

        # kann der Dialog umgangen werden um andere Fenster zu bedienen?
        d.setWindowModality(Qt.ApplicationModal) # nein (Standard)
        # d.setWindowModality(qc.Qt.WindowModal)    # ja

        # ... wie QWidget verwendbar
        fbox = QFormLayout()

        input_name = QLabel("YOU DIED")
        fbox.addRow("LOOSER", input_name)
        
        highscore = QLabel(str(self.snake.highscore))
        fbox.addRow("But your highscore was: ", highscore)

        btnok = QPushButton("Restart the Game",d)
        btnno = QPushButton("Quit",d)
        fbox.addRow(btnok, btnno)

        d.setLayout(fbox)

        # akzeptieren / ablehnen
        btnok.clicked.connect(lambda: d.accept())
        btnno.clicked.connect(lambda: d.reject())

        # bei Fehler / Erfolg an Hauptfenster melden
        d.accepted.connect(lambda: self.snake.reset_highscore())
        d.rejected.connect(lambda: self.close())

        # Extras
        btnok.setDefault(True)           # btn wird bei Enter gedrückt
        d.exec_()

    def render(self):
        self.draw_canvas()
        self.draw_background()
        self.snake.draw(self.snake_ebene, self.painter_snake, self.brush)
        self.fruit.draw(self.fruit_ebene, self.painter_fruit, self.brush)
        if self.snake.dead:
            self.died()

        self.painter_canvas.drawImage(0, 0, self.background)
        self.painter_canvas.drawImage(0, 0, self.snake_ebene)
        self.painter_canvas.drawImage(self.fruit.pos[0], self.fruit.pos[1], self.fruit_ebene)
        self.label.setPixmap(QPixmap.fromImage(self.canvas)) 