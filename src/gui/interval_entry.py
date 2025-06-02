import ttkbootstrap as ttk


from src.plc_connection import IntervalUnit


class IntervalEntry(ttk.Frame):
    def __init__(self, parent, interval_text_variable, interval_start_time_hour, interval_start_time_minute,
                 interval_unit_entry_variable
                 ):

        super().__init__(master=parent)
        self.parent = parent
        self.interval_text_variable = interval_text_variable
        self.interval_start_time_hour = interval_start_time_hour
        self.interval_start_time_minute = interval_start_time_minute
        self.interval_unit_entry_variable = interval_unit_entry_variable
        self.start_time_validation_message = "hour 0-23             minute 0-59"
        self.interval_validation_message = ""


        #---------- Interval Start Time Entry (Top Row) -----------#

        self.validation_frame = ttk.Frame(self)
        self.validation_frame.pack(expand=True, fill="both")

        # Validation message
        self.start_validation_label = ttk.Label(self.validation_frame, text="", foreground="red", justify='right')
        self.start_validation_label.pack(fill="both", side="right")

        # Top Frame
        self.top_frame = ttk.Frame(master=self)
        self.top_frame.pack(expand=True, fill="both")

        self.start_time_label = ttk.Label(master=self.top_frame, text="Interval Start Time:")
        self.start_time_label.pack(side="left", expand=True, fill="both", padx=(0,10) )

        self.minute_spinbox = ttk.Spinbox(master=self.top_frame ,width=2,font="calibri 12", increment=1,
                                          from_=0, to=59, textvariable=self.interval_start_time_minute)
        self.minute_spinbox.pack(side="right")

        self.minute_label = ttk.Label(master=self.top_frame, text="Minute:")
        self.minute_label.pack(side="right", padx=(0,5))

        self.hour_spinbox = ttk.Spinbox(master=self.top_frame,width=2,font="calibri 12",
                                        increment=1, from_=0, to=23, textvariable=self.interval_start_time_hour)
        self.hour_spinbox.pack(side="right", padx=(0,5))

        self.hour_label = ttk.Label(master=self.top_frame, text="Hour:")
        self.hour_label.pack(side="right", fill="both", padx=(0,5))

        #---------------------------------------#


        # -------------- Interval Time Entry (Bottom row) ------------- #

        #Validation Message

        self.bottom_validation_frame = ttk.Frame(self)
        self.bottom_validation_frame.pack(expand=True, fill="both")

        self.interval_validation_frame = ttk.Frame(self.bottom_validation_frame)
        self.interval_validation_frame.pack(fill="both", side="right")

        self.interval_validation_label = ttk.Label(self.interval_validation_frame, text="", foreground="red", justify='right')
        self.interval_validation_label.pack(fill="both", expand=True, side="right")

        self.bottom_frame = ttk.Frame(master=self)
        self.bottom_frame.pack(expand=True, fill="both")

        self.interval_label = ttk.Label(master=self.bottom_frame, text="Interval:")
        self.interval_label.pack(side = "left",fill="both", expand=True, padx=(0,10))

        self.option_items = [IntervalUnit.MS, IntervalUnit.SEC, IntervalUnit.MIN]

        self.option_menu = ttk.OptionMenu(self.bottom_frame,self.interval_unit_entry_variable,
                                          self.interval_unit_entry_variable.get(),*self.option_items)
        self.option_menu.configure(width=4)

        self.option_menu.pack(side="right")

        self.interval_entry = ttk.Entry(self.bottom_frame, width=10, textvariable=self.interval_text_variable)
        self.interval_entry.pack(side="right", padx=(0,10))






    def show_validation_message(self):

        if self.interval_unit_entry_variable.get() == IntervalUnit.MS:
            self.interval_validation_message = "0-1000000"
        elif self.interval_unit_entry_variable.get() == IntervalUnit.SEC:
            self.interval_validation_message = "0-100000"
        else:
            self.interval_validation_message = "0-10000"


        self.start_validation_label.config(text=self.start_time_validation_message)
        self.interval_validation_label.config(text=self.interval_validation_message)

    def hide_validation_message(self):
        self.start_validation_label.config(text="")
        self.interval_validation_label.config(text="")
