import tkinter as tk
import ttkbootstrap as ttk


class Indicator(tk.Frame):
    def __init__(self, parent, display_text, color):
        super().__init__(master=parent.inside_frame)
        self.color = color
        self.display_text = display_text
        self.display_label = ttk.Label(self, text=self.display_text, font=f"calibri 15", justify="right")
        self.canvas = tk.Canvas(self, height=0, width=40)

        self.oval = self.canvas.create_oval(2,2, 20, 20, outline="#3b3b3b", fill=self.color, width=1)

        self.display_label.grid(column=0, row=0, sticky='ew', padx=(0,10))
        self.canvas.grid(column=1, row=0, sticky='nsew',pady=(3,0))

    def set_color(self, color):
        self.canvas.itemconfig(self.oval, fill=color)

    def get_name(self):

        return self.display_text