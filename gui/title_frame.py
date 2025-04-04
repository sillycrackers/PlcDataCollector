import tkinter as tk
import ttkbootstrap as ttk

from utils import *

class TitleFrame(ttk.Frame):
    def __init__(self, parent, text):

        self.text = text

        super().__init__(master = parent)

        title_logo_image = tk.PhotoImage(file=resource_path("data_icon.png"))
        self.title_image = ttk.Label(self, image=title_logo_image)
        self.title_image.image = title_logo_image
        self.title_image.pack(side="left", padx=20)
        self.title_label = ttk.Label(self, text=self.text, justify="left" ,font="calibri 28")
        self.title_label.pack(side="left")

