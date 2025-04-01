import tkinter as tk
import ttkbootstrap as ttk
from PIL.ImageOps import expand
from openpyxl.styles.fills import fills
from ttkbootstrap.scrolled import *

from gui.new_output_display import NewOutputDisplay
from gui.indicator import Indicator
from gui.colors import *


class RightBodyFrame(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(master=main_frame)

        self.main_frame = main_frame

        self.title_label = ttk.Label(master=self, text="Output Messages",font="calibri 14",justify="left")
        self.title_label.pack(fill="x")

        self.output = NewOutputDisplay(parent=self)
        self.output.pack(expand=True, fill="both")


