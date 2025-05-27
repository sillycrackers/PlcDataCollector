import ttkbootstrap as ttk
import datetime

class SpecificTimeEntry:
    def __init__(self, parent, hour_text_variable,minute_text_variable, row):

        self.parent = parent
        self.row = row
        self.hour_text_variable = hour_text_variable
        self.minute_text_variable = minute_text_variable

        self.data_entry_label = ttk.Label(master=self.parent, text="Specific Time:")
        self.data_entry_label.grid(row=self.row, column=0, sticky='w', padx=(0,10) )

        self.frame = ttk.Frame(master= self.parent)
        self.frame.grid(row=self.row, column = 1, sticky="ew")

        self.hour_label = ttk.Label(master=self.frame, text="Hour:")
        self.hour_label.pack(side="left", fill="both", expand=True)

        self.hour_spinbox = ttk.Spinbox(master=self.frame,width=2,font="calibri 12",
                                        increment=1, from_=0, to=23, textvariable=self.hour_text_variable)
        self.hour_spinbox.pack(side="left", expand=True)

        self.minute_label = ttk.Label(master=self.frame, text="Minute:")
        self.minute_label.pack(side="left", expand=True)

        self.minute_spinbox = ttk.Spinbox(master=self.frame,width=2,font="calibri 12", increment=1,
                                          from_=0, to=59, textvariable=self.minute_text_variable)
        self.minute_spinbox.pack(side="left")

    def get_selected_time(self):

        return datetime.time(hour=int(self.hour_spinbox.get()),minute=int(self.minute_spinbox.get()))


