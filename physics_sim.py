import tkinter as tk

class Ball:
    def __init__(self, diameter=0, ball_id=0):
        self.diameter = diameter
        self.ball_id = ball_id

        self.radius = self.diameter / 2
        self.x_pos = 0
        self.y_pos = 0

        #Place ball at 0 initially
        self.coord = (0,0,self.diameter,self.diameter)

    def update_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

        x0 = self.x_pos
        y0 = self.y_pos
        x1 = x0 + self.diameter
        y1 = y0 + self.diameter

        self.coord = (x0, y0, x1, y1)

    def draw_abs(self, canvas : tk.Canvas, x, y):

        canvas.moveto(self.ball_id, x, y)
        self.update_pos(x,y)

    def draw_rel(self, canvas : tk.Canvas, x, y):

        canvas.move(self.ball_id, x, y)
        self.update_pos(self.x_pos + x, self.y_pos + y)