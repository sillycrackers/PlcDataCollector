import tkinter as tk

from src.gui.main_frame import MainFrame
from src.utils import *
from src.file_management import *

def main():

    root = ttk.Window(themename="darkly", hdpi=False)
    root.option_add('*tearOff', 'false')
    root.minsize(width=600, height=600)
    logo_image = tk.PhotoImage(file=resource_path("src\\gui\\imgs\\data_icon_small.png"))
    root.iconphoto(False, logo_image)
    app = MainFrame(root)
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
    #Disable the Close Window Control
    root.protocol("WM_DELETE_WINDOW", lambda : disable_event(root))
    root.state('zoomed')
    app.run_app()

if __name__ == "__main__":
    main()
