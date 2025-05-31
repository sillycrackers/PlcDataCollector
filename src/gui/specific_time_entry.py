import ttkbootstrap as ttk
import datetime




class SpecificTimeEntry(ttk.Frame):
    def __init__(self, parent, hour_text_variable, minute_text_variable, has_validation=False, validation_message=""):

        super().__init__(master=parent)
        self.parent = parent
        self.hour_text_variable = hour_text_variable
        self.minute_text_variable = minute_text_variable
        self.has_validation = has_validation
        self.validation_message = validation_message

        # Validation
        self.validation_label = ttk.Label(self, text="", foreground="red", justify='right')
        self.validation_label.pack(fill="both", expand=True)

        ttk.Label(master=self, text="Specific Time:").pack(side="left",fill="both",expand=True, padx=(0,10) )

        ttk.Label(master=self, text="Hour:").pack(side="left", fill="both", expand=True)

        self.hour_spinbox = ttk.Spinbox(master=self,width=2,font="calibri 12",
                                        increment=1, from_=0, to=23, textvariable=self.hour_text_variable)
        self.hour_spinbox.pack(side="left", expand=True)

        self.minute_label = ttk.Label(master=self, text="Minute:")
        self.minute_label.pack(side="left", expand=True)

        self.minute_spinbox = ttk.Spinbox(master=self,width=2,font="calibri 12", increment=1,
                                          from_=0, to=59, textvariable=self.minute_text_variable)
        self.minute_spinbox.pack(side="left")

    def show_validation_message(self):
        self.validation_label.config(text=self.validation_message)

    def hide_validation_message(self):
        self.validation_label.config(text="")
