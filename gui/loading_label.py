import tkinter as tk
import ttkbootstrap as ttk

class LoadingLabel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.parent = parent

        #Variables
        self.font = "calibri 18 bold"
        self.font_color = "red"
        self.dots_text = ttk.StringVar()

        # Widgets
        self.inner_frame = ttk.Frame(self)
        self.inner_frame.pack(expand=True)

        self.loading_label = ttk.Label(self.inner_frame,text="Loading", font=self.font, foreground=self.font_color)
        self.loading_label.pack(side="left", fill="x", padx=(70,0))

        self.dots_label = ttk.Label(self.inner_frame,width=6, text="",textvariable=self.dots_text, font=self.font, foreground=self.font_color)
        self.dots_label.pack(side="left", expand=True, fill="x")

    def adjust_dots(self, num: int):

        output_string = ""

        for x in range(num):
            output_string += "."

        self.dots_text.set(output_string)