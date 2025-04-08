import ttkbootstrap as ttk
from tkinter import filedialog

from gui.text_entry_window import TextEntryWindow


class DataEntry:
    def __init__(self, parent_window, parent, label_text, text_variable, row, has_popup=False, popup_type=""):

        self.parent = parent
        self.label_text = label_text
        self.text_variable = text_variable
        self.row = row
        self.has_popup = has_popup
        #popup types include: "tag_entry", "file_dir"
        self.popup_type = popup_type
        self.parent_window = parent_window


        self.name_label = ttk.Label(self.parent, text=self.label_text)
        self.name_label.grid(row=self.row,column=0, sticky='w', padx=10)
        self.name_entry = ttk.Entry(self.parent, width=30, textvariable=self.text_variable)
        self.name_entry.grid(row=self.row,column=1, sticky='e', padx=5)

        if self.has_popup:
            self.popup_button = ttk.Button(self.parent, text="···", command= self.open_popup)
            self.popup_button.grid(row=self.row, column=2, sticky='ew')

    def open_popup(self):

        if self.popup_type == "tag_entry":
            t = TextEntryWindow(self.text_variable,self.parent_window)
        elif self.popup_type == "file_dir":
            file_dir = filedialog.askdirectory()

            if file_dir:
                self.text_variable.set(file_dir)

