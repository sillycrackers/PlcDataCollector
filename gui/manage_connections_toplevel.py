import tkinter as tk


from utils import *
from gui.manage_connections_frame import ManageConnectionsFrame
from file_management import *


class ManageConnectionsToplevel(ttk.Toplevel):
    def __init__(self, root_window, main_frame):
        super().__init__(master=root_window)

        self.logo_image = tk.PhotoImage(file=resource_path("gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.minsize(width=550,height=700)
        self.title("Manage Connections")

        self.root_window = root_window
        self.main_frame = main_frame

        manage_connections_frame = ManageConnectionsFrame(parent_window=self, main_frame=self.main_frame)

        manage_connections_frame.pack()

        self.position_center()

        # Make parent window disabled and make sure to run close method when closing this window
        self.transient(root_window)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.root_window.attributes('-disabled', 1)


    def close(self):
        self.root_window.attributes('-disabled', 0)
        self.destroy()
        self.main_frame.left_body_frame.populate_indicators()