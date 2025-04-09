import tkinter as tk

from PIL.ImageOps import expand

from utils import *
from gui.physics_sim_frame import PhysicsSimFrame
from file_management import *


class PhysicsSimToplevel(ttk.Toplevel):
    def __init__(self):
        super().__init__()

        self.logo_image = tk.PhotoImage(file=resource_path("gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.minsize(width=700,height=700)
        self.title("Physics Simulator")

        self.physics_sim_frame = PhysicsSimFrame(self)
        self.physics_sim_frame.pack(expand=True, fill='both')

