import tkinter as tk
import ttkbootstrap as ttk

from main_frame import MainFrame
import utils

def main():

    utils.update_registry()
    root = ttk.Window(themename='journal', hdpi=False)
    root.option_add('*tearOff', 'false')
    root.title("PLC Data Collector")
    logo_image = tk.PhotoImage(file=resource_path("data_icon.png"))
    root.iconphoto(False, logo_image)
    app = MainFrame(root)
    app.body_frame.populate_indicators()

    app.run_app()

if __name__ == "__main__":
    main()









