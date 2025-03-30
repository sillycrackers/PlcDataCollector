import tkinter as tk
import ttkbootstrap as ttk


from utils import *


class ManageConnectionsToplevel(ttk.Toplevel):
    def __init__(self, root_window, parent_frame):
        super().__init__(master=root_window)
        self.logo_image = tk.PhotoImage(file=resource_path("data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.minsize(width=550,height=550)
        self.resizable(width=False, height=False)
        self.title("Manage Connections")

        self.root_window = root_window
        self.parent_frame = parent_frame

        # Make parent window disabled and make sure to run close method when closing this window
        self.transient(root_window)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.root_window.attributes('-disabled', 1)


    def close(self):
        self.root_window.attributes('-disabled', 0)
        self.destroy()
        self.parent_frame.body_frame.populate_indicators()