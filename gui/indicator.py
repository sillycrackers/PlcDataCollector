import tkinter as tk
import ttkbootstrap as ttk

from utils import *


class Indicator(tk.Frame):
    def __init__(self, parent, display_text, color):
        super().__init__(master=parent.inside_frame)
        self.color = color

        self.display_text = display_text
        self.display_label = ttk.Label(self, text=self.display_text, font=f"calibri 16", justify="right")

        self.ind_icon_true = tk.PhotoImage(file=resource_path("green_check.png"))
        self.ind_icon_true_label = ttk.Label(self, image=self.ind_icon_true)

        self.ind_icon_false = tk.PhotoImage(file=resource_path("mark.png"))
        self.ind_icon_false_label = ttk.Label(self, image=self.ind_icon_false)

        self.current_icon_label = self.ind_icon_false_label

        self.display_label.pack(side="left")
        self.current_icon_label.pack(side="right")

    def set_state(self, state):
        if state:

            self.current_icon_label.pack_forget()
            self.current_icon_label = self.ind_icon_true_label
            self.current_icon_label.pack(side="right")
        else:
            self.current_icon_label.pack_forget()
            self.current_icon_label = self.ind_icon_false_label
            self.current_icon_label.pack(side="right")

    def get_name(self):

        return self.display_text