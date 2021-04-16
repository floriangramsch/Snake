from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class Snake:
    def __init__(self, x, y, width):
        self.body = [[x, y]]
        self.width = width
        self.vel = 0
        self.dir = [0, 0]
        self.dead = False
        self.highscore = 0

    def change_dir(self, dir):
        self.dir[0] = dir[0] * self.vel
        self.dir[1] = dir[1] * self.vel

    def get_head_pos(self):
        return self.body[0] 

    def move(self, board_width, passable_boarder):
        pos = self.get_head_pos()
        new_pos_x = pos[0] + self.dir[0]
        new_pos_y = pos[1] + self.dir[1]
        if [new_pos_x, new_pos_y] in self.body[1:]:
            self.reset()
        else:
            if len(self.body) == 1:
                self.body[0][0] = new_pos_x
                self.body[0][1] = new_pos_y
            else:
                self.body.insert(0, [new_pos_x, new_pos_y])
                self.body.pop()

        if not passable_boarder:
            if pos[0] < 0 or pos[0] + self.width > board_width or pos[1] < 0 or pos[1] + self.width > board_width:
                self.reset()
        else:
            if pos[0] < 0:
                self.body[0][0] = board_width - self.width
            if pos[0] >= board_width:
                self.body[0][0] = 0

            if pos[1] < 0:
                self.body[0][1] = board_width - self.width
            if pos[1]>= board_width:
                self.body[0][1] = 0

    def reset(self):
            self.highscore = len(self.body) - 1
            self.vel = 0
            self.change_dir([0, 1])
            self.body = [[0, 0]]
            self.dead = True

    def draw(self, ebene, painter, brush):
        ebene.fill(Qt.transparent)
        brush.setStyle(Qt.SolidPattern)

        ## HEAD
        brush.setColor(QtGui.QColor('blue'))
        painter.setBrush(brush)
        painter.drawRoundedRect(self.body[0][0], self.body[0][1], self.width, self.width, 10.0, 10.0)

        ## BODY
        brush.setColor(QtGui.QColor('red'))
        painter.setBrush(brush)
        for i in self.body[1:]:
            # painter.drawRect(i[0], i[1], self.snake.width, self.snake.width)
            painter.drawRoundedRect(i[0], i[1], self.width, self.width, 10.0, 10.0)

    def add_length(self):
        pos = self.get_head_pos()
        new_pos_x = pos[0] - self.dir[0]
        new_pos_y = pos[1] - self.dir[1]
        self.body.append([new_pos_x, new_pos_y])

    def revive(self):
        self.dead = False

    def reset_highscore(self):
        self.highscore = 0