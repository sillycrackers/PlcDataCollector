import ttkbootstrap as ttk
import datetime

class IntervalEntry:
    def __init__(self, parent, interval_text_variable, interval_start_time_hour, interval_start_time_minute, row):

        self.parent = parent
        self.row = row
        self.interval_text_variable = interval_text_variable
        self.interval_start_time_hour = interval_start_time_hour
        self.interval_start_time_minute = interval_start_time_minute


        #---------- Interval Start Time Entry -----------#

        self.start_time_label = ttk.Label(master=self.parent, text="Interval Start Time:")
        self.start_time_label.grid(row=self.row, column=0, sticky='w', padx=(0,10) )

        self.frame = ttk.Frame(master= self.parent)
        self.frame.grid(row=self.row, column = 1, sticky="ew")

        self.hour_label = ttk.Label(master=self.frame, text="Hour:")
        self.hour_label.pack(side="left", fill="both", expand=True)

        self.hour_spinbox = ttk.Spinbox(master=self.frame,width=2,font="calibri 12",
                                        increment=1, from_=0, to=23, textvariable=self.interval_start_time_hour)
        self.hour_spinbox.pack(side="left", expand=True)

        self.minute_label = ttk.Label(master=self.frame, text="Minute:")
        self.minute_label.pack(side="left", expand=True)

        self.minute_spinbox = ttk.Spinbox(master=self.frame,width=2,font="calibri 12", increment=1,
                                          from_=0, to=59, textvariable=self.interval_start_time_minute)
        self.minute_spinbox.pack(side="left")

        #---------------------------------------#

        #------------ Interval Time Entry (Next row) -------------#

        self.row += 1




    def get_selected_time(self):

        return datetime.time(hour=int(self.hour_spinbox.get()),minute=int(self.minute_spinbox.get()))


