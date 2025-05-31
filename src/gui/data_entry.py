import ttkbootstrap as ttk
from tkinter import filedialog

from src.gui.text_entry_window import TextEntryWindow


class DataEntry(ttk.Frame):

    def __init__(self, parent_window, parent, label_text, text_variable, has_popup=False, popup_type="",
                 has_validation=False, validation_message=""):

        super().__init__(master=parent)

        self.parent = parent
        self.label_text = label_text
        self.text_variable = text_variable
        self.has_popup = has_popup
        #popup types include: "tag_entry", "file_dir"
        self.popup_type = popup_type
        self.parent_window = parent_window
        self.has_validation = has_validation
        self.validation_message = validation_message

        # Name Validation
        self.validation_label = ttk.Label(self, text="", foreground="red", justify='right')
        self.validation_label.pack(fill="both", expand=True)

        self.data_entry_label = ttk.Label(self, text=self.label_text)
        self.data_entry_label.pack(side="left", fill="both", expand=True, padx=(0,10))

        self.data_entry = ttk.Entry(self, width=30, textvariable=self.text_variable)
        self.data_entry.pack(side="right", fill="both", expand=True, padx=5)


        if self.has_popup:
            self.popup_button = ttk.Button(self.parent, text="···", command= self.open_popup)
            self.popup_button.pack(side="right")

    def open_popup(self):

        if self.popup_type == "tag_entry":
            t = TextEntryWindow(self.text_variable,self.parent_window)
        elif self.popup_type == "file_dir":
            file_dir = filedialog.askdirectory()

            if file_dir:
                self.text_variable.set(file_dir)


    def show_validation_message(self):
        self.validation_label.config(text=self.validation_message)

    def hide_validation_message(self):
        self.validation_label.config(text="")