import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk

import src.file_management as fm


class ExitPrompt(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.parent = parent
        self.logo_image = tk.PhotoImage(file=fm.resource_path("src\\gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.title("Prompt")

        self.resizable(width=False, height=False)

        #main frame for window
        self.frame = ttk.Frame(self)
        self.frame.pack(expand=True, fill="both")

        #frame for message and x image
        self.label_frame = ttk.Frame(self.frame)
        self.label_frame.pack(expand=True, padx=50, pady=50)

        #Make new smaller image
        self.img = Image.open(fm.resource_path("src\\gui\\imgs\\red_x.png"))
        self.resized_img = ImageTk.PhotoImage(self.img.resize(size=(50,50),resample=Image.Resampling.LANCZOS))
        self.img.close()

        #Message and x image
        self.label = ttk.Label(self.label_frame, text="Do you really want to exit?\nPress 'Ctrl e' to exit", font="Calibri 24", justify="center")
        self.label.pack(side="left")
        self.x_image_label = ttk.Label(self.label_frame, image=self.resized_img)
        self.x_image_label.pack(side="right", padx=(30,10), pady=(3,0), expand=True)

        #Ok button to exit
        self.ok_button = ttk.Button(self.frame, text="Ok", style='custom.TButton', width=10, command=self.close)
        self.ok_button.pack(side="bottom", padx=20, pady=(0,40))

        # Make parent window disabled and make sure to run close method when closing this window
        self.transient(self.parent)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.parent.attributes('-disabled', 1)

        self.position_center()

    def close(self):
        self.parent.attributes('-disabled', 0)
        self.destroy()
