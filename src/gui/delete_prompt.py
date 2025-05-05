import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

import src.file_management as fm


class DeletePrompt(ttk.Toplevel):
    def __init__(self, parent, parent_window, plc_name, response_callback):
        super().__init__(master=parent)
        self.parent_window = parent_window
        self.logo_image = tk.PhotoImage(file=fm.resource_path("src\\gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.minsize(width=500, height=250)
        self.title("Prompt")
        self.plc_name = plc_name
        self.response_callback = response_callback

        self.response = False

        self.resizable(width=False, height=False)

        #main frame for window
        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True, fill="both", pady=(0,20))

        #frame for message and x image
        self.label_frame = ttk.Frame(self.frame)
        self.label_frame.pack(expand=True, padx=30, pady=20)

        #Make new smaller image
        self.img = Image.open(fm.resource_path("src\\gui\\imgs\\red_x.png"))
        self.resized_img = ImageTk.PhotoImage(self.img.resize(size=(50,50),resample=Image.Resampling.LANCZOS))
        self.img.close()

        #Message and x image
        self.label = ttk.Label(self.label_frame, text=f"Do you really want to delete:\n{self.plc_name}?", font="Calibri 24", justify="left")
        self.label.pack(side="left")
        self.x_image_label = ttk.Label(self.label_frame, image=self.resized_img)
        self.x_image_label.pack(side="right", padx=(30,10), pady=(3,0), expand=True)

        #No Button
        self.no_button = ttk.Button(self.frame, text="No", style='custom.TButton', width=10, command=lambda : self.callback(False))
        self.no_button.pack(side="bottom", padx=20, pady=(0,0))
        #Yes Button
        self.yes_button = ttk.Button(self.frame, text="Yes", style='custom.TButton', width=10, command=lambda : self.callback(True))
        self.yes_button.pack(side="bottom", padx=20, pady=(0,30))


        # Make parent window disabled and make sure to run close method when closing this window
        self.transient(self.parent_window)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.parent_window.attributes('-disabled', 1)

        self.position_center()

    def close(self):
        self.parent_window.attributes('-disabled', 0)
        self.destroy()

    def callback(self, response):
        self.response_callback(response)
        self.close()