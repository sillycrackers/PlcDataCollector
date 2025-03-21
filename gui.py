import tkinter as tk
import ttkbootstrap as ttk
import winreg


from main_frame import MainFrame
from utils import *

def update_registry():

    icon_path = file=resource_path("data_icon.ico")
    try:

        pdc_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'.pdc\DefaultIcon')
        winreg.SetValueEx(pdc_key,'',0, winreg.REG_SZ, icon_path)
        if pdc_key:
            winreg.CloseKey(pdc_key)
        return True
    except WindowsError:
        print("Cannot change registry")
        return False


def main():
    '''
    dark themes: solar, superhero, darkly, cyborg, vapor
    light themes: cosmo, flatly, journal, litera, lumen, minty, pulse, sandstone, united, yeti, morph, simplex, cerculean,
    '''

    #Trying to get Git working

    update_registry()
    root = ttk.Window(themename='journal', hdpi=False)
    root.option_add('*tearOff', 'false')
    root.title("PLC Data Collector")
    logo_image = tk.PhotoImage(file=resource_path("data_icon.png"))
    root.iconphoto(False, logo_image)
    #root.resizable(False, False)

    dpi = root.winfo_fpixels('1i')

    app = MainFrame(root)
    #app.add_plc_connection(PlcConnection(hino_slinger_plc))
    #app.add_plc_connection(PlcConnection(cnc_op10_plc))
    app.body_frame.populate_indicators()

    app.run_app()

if __name__ == "__main__":
    main()









