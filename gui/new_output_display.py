import tkinter as tk
from idlelib.configdialog import font_sample_text


import ttkbootstrap as ttk
from ttkbootstrap.scrolled import *

class NewOutputDisplay(ttk.Frame):
    def __init__(self, parent, style = None):
        super().__init__(master=parent)

        self.iid_count = 0

        self.at_bottom = True

        self.scrollbar = ttk.Scrollbar(self)
        self.listbox = ttk.Treeview(self, yscrollcommand=self.scrollbar.set, show="tree")
        self.scrollbar.configure(command=self.call_back)
        self.style = style

        if self.style is not None:
            self.listbox.configure(style=self.style)

        self.scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", expand=True, fill="both")

        for x in range(2000):
            self.add_message("Hello World")


    def call_back(self, *args):

        if float(args[1]) > 0.9:
            self.at_bottom = True
            print("At bottom")
        else:
            self.at_bottom = False
            print("Not at bottom")

        self.listbox.yview(*args)

    def add_message(self, message):
        self.iid_count += 1
        self.listbox.insert(parent='',index="end",text=message,iid=self.iid_count)

        if self.at_bottom:
            self.listbox.yview_moveto(1)
            self.at_bottom = True

    def clear_messages(self):

        if self.iid_count > 1:
            self.iid_count -= 1

        if self.iid_count > 0:
            for item in self.listbox.get_children():
                self.listbox.delete(item)