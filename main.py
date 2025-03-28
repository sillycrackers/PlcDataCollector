import tkinter as tk
import ttkbootstrap as ttk
import webbrowser
new = 2 # open in a new tab, if possible

from gui.main_frame import MainFrame
import utils

def main():

    root = ttk.Window(themename='journal', hdpi=False)

    root.option_add('*tearOff', 'false')
    root.title("PLC Data Collector")
    logo_image = tk.PhotoImage(file=utils.resource_path("data_icon.png"))
    root.iconphoto(False, logo_image)
    app = MainFrame(root)
    app.body_frame.populate_indicators()


    app.run_app()

if __name__ == "__main__":
    main()









