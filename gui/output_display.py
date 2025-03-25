import tkinter as tk
from idlelib.configdialog import font_sample_text

import ttkbootstrap as ttk
from ttkbootstrap.scrolled import *

class OutputDisplay(ScrolledFrame):
    def __init__(self, parent, font_color):
        super().__init__(master=parent)

        self.font_color = font_color

        self.listbox = tk.Listbox(self, foreground=self.font_color, font='calibri 14')

        self.listbox.pack(expand=True, fill="both")

        self.pack(expand=True, fill="both")

    def add_message(self, message):
        self.listbox.insert("end",message)
        self.listbox.itemconfig("end", {'fg': 'red'})

    def clear_messages(self):
        self.listbox.delete('0','end')