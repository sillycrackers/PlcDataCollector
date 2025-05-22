import tkinter as tk
import ttkbootstrap as ttk

from src.gui.manage_connections_frame import ManageConnectionsFrame
import src.file_management as fm


class ManageConnectionsToplevel(ttk.Toplevel):
    def __init__(self, root_window, main_frame):
        super().__init__(master=root_window)

        self.logo_image = tk.PhotoImage(file=fm.resource_path("src\\gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.minsize(width=550,height=720)
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


    def close(self, data_changed=False):
        self.root_window.attributes('-disabled', 0)
        self.destroy()
        if data_changed:
            self.main_frame.left_body_frame.populate_indicators()