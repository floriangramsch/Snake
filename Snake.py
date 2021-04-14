class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 50

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.vel = 8

    def change_dir(self, dir):
        if dir == "Left":
            self.left = True
            self.right, self.up, self.down = False, False, False
        if dir == "Right":
            self.right = True
            self.left, self.up, self.down = False, False, False
        if dir == "Down":
            self.down = True
            self.right, self.up, self.left = False, False, False
        if dir == "Up":
            self.up = True
            self.right, self.left, self.down = False, False, False

    def move(self):
        if self.left:
            self.x -= self.vel
        if self.right:
            self.x += self.vel
        if self.down:
            self.y += self.vel
        if self.up:
            self.y -= self.vel