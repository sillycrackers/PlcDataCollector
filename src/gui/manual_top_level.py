import tkinter as tk
import ttkbootstrap as ttk



import src.utils as utils
import src.file_management as fm


class ManualTopLevel(tk.Toplevel):
    def __init__(self, root_window, main_frame):
        super().__init__(master=root_window)

        self.logo_image = tk.PhotoImage(file=fm.resource_path("src\\gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.title("Manual")
        self.root_window = root_window
        self.main_frame = main_frame
        self.state("zoomed")


        # Make parent window disabled and make sure to run close method when closing this window
        self.transient(root_window)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.root_window.attributes('-disabled', 1)


        #Main Wrapper Frame for all content
        self.wrapper_frame = tk.Frame(master=self, background="#a3a3a3")
        self.wrapper_frame.pack(expand=True, fill="both")



    def close(self):
        self.root_window.attributes('-disabled', 0)
        self.destroy()