import ttkbootstrap as ttk

from src.plc_connection import TriggerType


class TriggerSelectEntry:
    def __init__(self, parent, text_variable, row, command):

        self.parent = parent
        self.row = row
        self.text_variable = text_variable

        self.option_items = ["PLC Trigger", "Specific Time", "Time Interval"]

        self.data_entry_label = ttk.Label(master=self.parent, text="Trigger Type:")
        self.data_entry_label.grid(row=self.row, column=0, sticky='w', padx=(0,10) , pady=(20,0))

        self.option_menu = ttk.OptionMenu(self.parent,self.text_variable,
                                          self.text_variable.get(),*self.option_items,
                                          command=lambda _: command())
        self.option_menu.configure(width=18)

        self.option_menu.grid(row=self.row, column=1, sticky='e', padx=(0,5), pady=(20,0))
