import tkinter as tk

from src.utils import *
from src.file_management import *


class AboutWindow(ttk.Toplevel):
    def __init__(self, parent_window):
        super().__init__(master=parent_window)
        self.parent_window = parent_window
        self.title("About PLC Data Collector")
        self.logo_image = tk.PhotoImage(file=resource_path("src\\gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.geometry("400x220")
        self.resizable(width=False, height=False)

        #Main Frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        #Logo Image
        self.logo_image = tk.PhotoImage(file=resource_path("src\\gui\\imgs\\data_icon.png"))
        self.logo_image_label = ttk.Label(self.main_frame, image=self.logo_image)
        self.logo_image_label.grid(row=0,column=0, padx=20, pady=20)

        #Label Frame
        self.label_frame = ttk.Frame(self.main_frame)
        self.label_frame.grid(row=0, column=1, sticky='ew', padx=30)

        self.about_label_title = ttk.Label(self.label_frame, text="PLC Data Collector", font="calibri 16")
        self.about_label_title.pack(pady=20)
        self.about_label_body = ttk.Label(self.label_frame, text='Version 1.0\n\nCopyright © 2025 Erik Westerveld',justify='center')
        self.about_label_body.pack()

        self.close_button = ttk.Button(self.main_frame, text="Close", command=self.close, width=20)
        self.close_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.transient(self.parent_window)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.parent_window.attributes('-disabled', 1)


    def close(self):
        self.parent_window.attributes('-disabled', 0)
        self.destroy()
