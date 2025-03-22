import os
import sys
import winreg
import ttkbootstrap as ttk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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


def change_theme(theme):
    if theme == 'dark':
        ttk.Style(theme='darkly')
    elif theme == 'light':
        ttk.Style(theme='flatly')

