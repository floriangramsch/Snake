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
        self.vel = QSlider(Qt.Horizontal)
        # self.vel.setMinimum(10)
        # self.vel.setMaximum(1)
        self.vel.setRange(1, 10); 
        self.vel.setValue(2)
        self.vel.setInvertedAppearance(True)

        self.game_size = QSlider(Qt.Horizontal)
        self.game_size.setMinimum(10)
        self.game_size.setMaximum(100)
        self.game_size.setValue(16)

        self.border = QCheckBox()

        self.fruit_probabilty = QSlider(Qt.Horizontal)
        self.fruit_probabilty.setRange(0, 100)

        self.hidden = False

        # self.vbox = QVBoxLayout(self)
        # self.vbox.addWidget(self.label)
        # self.vbox.addWidget(self.vel)
        self.fbox.addRow("Velocity:", self.vel)
        self.fbox.addRow("Game Size:", self.game_size)
        self.fbox.addRow("Passing border? :", self.border)
        self.fbox.addRow("Props. of Fruits:", self.fruit_probabilty)

        self.vbox.addWidget(QLabel("Settings"))
        self.vbox.addLayout(self.fbox)
        self.setLayout(self.vbox)