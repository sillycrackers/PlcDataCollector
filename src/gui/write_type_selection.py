import ttkbootstrap as ttk

from src.plc_connection import WriteType

class WriteTypeSelect(ttk.Frame):
    def __init__(self, parent, selected_variable):
        super().__init__(master=parent)

        self.parent = parent
        self.selected_variable = selected_variable

        self.label = ttk.Label(self, text="Write Type Select:")
        self.label.pack(side="left", padx=(0,10))

        self.radio_button_append = ttk.Radiobutton(self, text="Append", variable=self.selected_variable, value=WriteType.APPEND)
        self.radio_button_overwrite = ttk.Radiobutton(self, text="Overwrite", variable=self.selected_variable, value=WriteType.OVERWRITE)

        self.radio_button_append.pack(side="left", expand=True, fill="both", padx=10)
        self.radio_button_overwrite.pack(side="left", expand=True, fill="both", padx=10)

