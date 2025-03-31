import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import *

from gui.new_output_display import NewOutputDisplay
from gui.output_display import OutputDisplay
from gui.indicator import Indicator
from gui.colors import *


class RightBodyFrame(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(master=main_frame)

        self.main_frame = main_frame

        self.label_frame = ttk.LabelFrame(master=self,text="Message Output")
        self.label_frame.pack(expand=True, fill="both")

        self.output = NewOutputDisplay(self.label_frame)
        self.output.pack()
