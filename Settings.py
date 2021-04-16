from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSlider, QLineEdit, QFormLayout, QCheckBox
from PyQt5.QtCore import Qt
# from PyQt5.QtGui import 

class Settings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # self.setStyleSheet("border: 1px solid black;")

        self.vbox = QVBoxLayout()
        self.fbox = QFormLayout()

        self.label = QLabel("Settings")

        ## VELOCITY
        self.vel = QSlider(Qt.Horizontal)
        self.vel.setRange(1, 10); 
        self.vel.setValue(2)
        self.vel.setInvertedAppearance(True)

        ## GAME SIZE
        self.game_size = QSlider(Qt.Horizontal)
        self.game_size.setMinimum(10)
        self.game_size.setMaximum(100)
        self.game_size.setValue(16)

        ## CAN YOU PASS THE BORDER?
        self.border = QCheckBox()
        self.border.setChecked(True)

        ## PROBABILITY OF FRUITS
        self.fruit_probability = QSlider(Qt.Horizontal)
        self.fruit_probability.setRange(0, 100)

        ## ARE THE SETTINGS HIDDEN?
        self.hidden = True

        ## POSITIONS
        self.snake_x = QLabel()
        self.snake_y = QLabel()
        self.fruit_x = QLabel()
        self.fruit_y = QLabel()

        # self.vbox = QVBoxLayout(self)
        # self.vbox.addWidget(self.label)
        # self.vbox.addWidget(self.vel)
        self.fbox.addRow(self.snake_x, self.snake_y)
        self.fbox.addRow(self.fruit_x, self.fruit_y)
        self.fbox.addRow("Velocity:", self.vel)
        self.fbox.addRow("Game Size:", self.game_size)
        self.fbox.addRow("Donut Version? :", self.border)
        self.fbox.addRow("Props. of Fruits:", self.fruit_probability)

        self.vbox.addWidget(QLabel("Settings"))
        self.vbox.addLayout(self.fbox)
        self.setLayout(self.vbox)