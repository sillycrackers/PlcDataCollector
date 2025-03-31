import tkinter as tk
from idlelib.configdialog import font_sample_text


import ttkbootstrap as ttk
from ttkbootstrap.scrolled import *

class NewOutputDisplay(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.scrollbar = ttk.Scrollbar(self)
        self.listbox = ttk.Treeview(self, yscrollcommand=self.scrollbar.set, show="tree")
        self.scrollbar.configure(command=self.listbox.yview)

        self.scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", expand=True, fill="both")

        self.pack(expand=True, fill="both")

        for x in range(10):
            self.add_message("Hello", x)

    def add_message(self, message, iid):
        self.listbox.insert(parent='',index="end",text=message,iid=iid)

    def clear_messages(self):
        self.listbox.delete('0','end')