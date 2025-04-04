import tkinter as tk
import ttkbootstrap as ttk

from gui.main_frame import MainFrame

from utils import *

def main():

    root = ttk.Window(themename='journal', hdpi=False)

    root.option_add('*tearOff', 'false')
    root.minsize(width=800,height=600)
    root.title("PLC Data Collector")
    logo_image = tk.PhotoImage(file=resource_path("data_icon.png"))
    root.iconphoto(False, logo_image)
    app = MainFrame(root)
    root.bind_all("<Button-1>", lambda event: event.widget.focus_set())
    # Disable the Close Window Control Icon
    #root.protocol("WM_DELETE_WINDOW", disable_event)

    app.run_app()

if __name__ == "__main__":
    main()

