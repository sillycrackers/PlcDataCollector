import ttkbootstrap as ttk


from src.plc_connection import IntervalUnit


class IntervalEntry:
    def __init__(self, parent, interval_text_variable, interval_start_time_hour,
                 interval_start_time_minute, interval_unit_entry_variable, row):

        self.parent = parent
        self.row = row
        self.interval_text_variable = interval_text_variable
        self.interval_start_time_hour = interval_start_time_hour
        self.interval_start_time_minute = interval_start_time_minute
        self.interval_unit_entry_variable = interval_unit_entry_variable


        #---------- Interval Start Time Entry -----------#

        self.start_time_label = ttk.Label(master=self.parent, text="Interval Start Time:")
        self.start_time_label.grid(row=self.row, column=0, sticky='w', padx=(0,10) )

        self.start_time_frame = ttk.Frame(master= self.parent)
        self.start_time_frame.grid(row=self.row, column = 1, sticky="ew")

        self.hour_label = ttk.Label(master=self.start_time_frame, text="Hour:")
        self.hour_label.pack(side="left", fill="both", expand=True)

        self.hour_spinbox = ttk.Spinbox(master=self.start_time_frame,width=2,font="calibri 12",
                                        increment=1, from_=0, to=23, textvariable=self.interval_start_time_hour)
        self.hour_spinbox.pack(side="left", expand=True)

        self.minute_label = ttk.Label(master=self.start_time_frame, text="Minute:")
        self.minute_label.pack(side="left", expand=True)

        self.minute_spinbox = ttk.Spinbox(master=self.start_time_frame,width=2,font="calibri 12", increment=1,
                                          from_=0, to=59, textvariable=self.interval_start_time_minute)
        self.minute_spinbox.pack(side="left")

        #---------------------------------------#

        #------------ Interval Time Entry (Next row) -------------#


        self.interval_label = ttk.Label(master=self.parent, text="Interval:")
        self.interval_label.grid(row=self.row + 1, column=0, sticky="w", padx=(0,10))

        self.interval_frame = ttk.Frame(master=self.parent)
        self.interval_frame.grid(row=self.row + 1, column = 1, sticky="nsew")

        self.interval_entry = ttk.Entry(self.interval_frame, width=10, textvariable=self.interval_text_variable)
        self.interval_entry.pack(side="left", padx=5, fill="both", expand=True)

        self.option_items = [IntervalUnit.MS, IntervalUnit.SEC, IntervalUnit.MIN]

        self.option_menu = ttk.OptionMenu(self.interval_frame,self.interval_unit_entry_variable,
                                          self.interval_unit_entry_variable.get(),*self.option_items)
        self.option_menu.configure(width=5)

        self.option_menu.pack(side="left", padx=5, fill="both", expand=True)

