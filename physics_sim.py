import tkinter as tk

class Ball:
    def __init__(self, radius=0, ball_id=0):
        self.radius = radius

        self.x = 0
        self.y = 0

        self.current_speed = 0

    def set_pos(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos

    def draw_abs(self, x, y):

        self.set_pos(x,y)

    def draw_rel(self, x, y):

        self.set_pos(self.x + x, self.y + y)

    def get_coord(self):

        return self.x, self.y