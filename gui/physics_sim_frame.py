from utils import *
import tkinter as tk


class PhysicsSimFrame(ttk.Frame):

    def __init__(self, parent_window):
        super().__init__(master=parent_window)

        self.parent_window = parent_window

        self.canvas = ttk.Canvas(self, width=400, height=400)
        self.canvas.config(bg="light grey")
        self.canvas.pack(expand=True)

        c_width = self.canvas.winfo_reqwidth()
        c_height = self.canvas.winfo_reqheight()

        ball_size = 50

        ball_radius = ball_size / 2

        #Place ball in center of canvas

        ball_x_pos = 0.25
        ball_y_pos = 0.50

        ball_x0 = ball_x_pos * c_width
        ball_y0 = ball_y_pos * c_height

        ball_coord = (ball_x0 - ball_radius, ball_y0 - ball_radius, ball_x0 + ball_radius, ball_y0 + ball_radius)

        #Center x = (x1 - x0) / 2
        #Center Y = (y1 - y0) / 2

        #(x0, y0, x1, y1)
        #x1 = x0 + ball_size
        #y1 = y0 + ball_size

        self.canvas.create_oval(ball_coord, fill="red")

        self.drop_button = ttk.Button(self, text="Drop Ball", width=15)
        self.drop_button.pack(pady=(20,50))


class Ball:
    def __init__(self, diameter):
        self.diameter = diameter

        self.radius = self.diameter / 2
        self.x_pos = 0
        self.y_pos = 0

    def set_pos(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

