import tkinter as tk

from gui.main_frame import MainFrame
from utils import *
from file_management import *

def main():

    root = ttk.Window(themename="darkly", hdpi=False)
    root.option_add('*tearOff', 'false')
    root.minsize(width=600,height=600)
    root.title("PLC Data Collector")
    logo_image = tk.PhotoImage(file=resource_path("gui/imgs/data_icon_small.png"))
    root.iconphoto(False, logo_image)
    app = MainFrame(root)
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
    #Disable the Close Window Control
    #root.protocol("WM_DELETE_WINDOW", lambda : disable_event(root))
    #change_theme("dark")
    root.state('zoomed')

    app.run_app()


if __name__ == "__main__":
    main()

