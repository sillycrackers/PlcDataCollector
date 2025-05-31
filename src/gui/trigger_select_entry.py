import ttkbootstrap as ttk

from src.plc_connection import TriggerType


class TriggerSelectEntry(ttk.Frame):
    def __init__(self, parent, text_variable, command):

        super().__init__(master=parent)
        self.parent = parent
        self.text_variable = text_variable

        self.option_items = ["PLC Trigger", "Specific Time", "Time Interval"]

        self.data_entry_label = ttk.Label(master=self, text="Trigger Type:")
        self.data_entry_label.pack(side="left", expand=True, fill="both", padx=(0,10) , pady=(20,0))

        self.option_menu = ttk.OptionMenu(self,self.text_variable,
                                          self.text_variable.get(),*self.option_items)
        self.option_menu.configure(width=18)

        self.option_menu.pack(side="right", expand=True, fill="both", padx=(0,5), pady=(20,0))
