from utils import *
import tkinter as tk

from physics_sim import *


class PhysicsSimFrame(ttk.Frame):

    def __init__(self, parent_window):
        super().__init__(master=parent_window)

        self.parent_window = parent_window

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.config(bg="light grey")
        self.canvas.pack(expand=True)

        c_width = self.canvas.winfo_reqwidth()
        c_height = self.canvas.winfo_reqheight()


        #Place ball in center of canvas

        self.ball1 = Ball(diameter=50)
        self.ball1.ball_id = self.canvas.create_oval(self.ball1.coord, fill="red")

        #middle of canvas
        center_x = (c_width/2) - self.ball1.radius
        center_y =  (c_height/2) - self.ball1.radius

        #Top middle of canvas
        self.ball1.draw_abs(canvas=self.canvas,x=center_x,y=0)

        self.move_button = ttk.Button(self, text="Move Ball", width=15,
                                      command= lambda : self.move_ball(ball=self.ball1, canvas=self.canvas))
        self.move_button.pack(pady=(20,50))

    def move_ball(self, ball : Ball, canvas : tk.Canvas):

        ball.draw_rel(canvas, 0, 5)

        if not (ball.y_pos + ball.diameter == self.canvas.winfo_reqheight()):
            self.after(50, lambda : self.move_ball(ball=self.ball1, canvas=self.canvas))







