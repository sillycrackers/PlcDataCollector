import tkinter as tk
from ttkbootstrap.scrolled import *

from src.gui.new_output_display import NewOutputDisplay
from src.gui.indicator import Indicator
from src.gui.colors import *
from src import utils



class LeftBodyFrame(ttk.Frame):
    def __init__(self,parent_frame, main_frame):
        super().__init__(master=parent_frame)
        #change_theme("dark")

        self.main_frame = main_frame
        self.parent_frame = parent_frame

        self.indicators = {}

        self.title_label = ttk.Label(self, text="PLC Connections", font="calibri 14", justify="left")
        self.title_label.pack(fill='x')

        self.border_frame = ttk.Frame(self, borderwidth=1, relief=tk.SOLID)
        self.border_frame.pack(fill="both", expand=True)

        self.scrolled_frame = ScrolledFrame(self.border_frame)
        self.scrolled_frame.pack(fill="both", expand=True)

        self.indicator_frame = ttk.Frame(self.scrolled_frame, style="custom.TFrame")
        self.indicator_frame.pack(fill="y", expand=True)

        self.open_manage_connections_button = ttk.Button(self,style='custom.TButton', text="Manage Connections", command=self.main_frame.open_manage_connections_window)
        self.open_manage_connections_button.pack(pady=(10,10))

        self.alarm_title = ttk.Label(self, text="Active Alarms", font="calibri 14", foreground='red', justify="left")
        self.alarm_title.pack(fill="x")

        self.alarm_output = NewOutputDisplay(self, style='alarm.Treeview')
        self.alarm_output.pack(expand=True, fill="both")

    #Create and display indicators the indicators for all connections
    #First we clear the current displayed indicators and make a new dictionary of the required indicators
    #The reason for using a dictionary instead of a list is so we can toggle specific ones later
    def populate_indicators(self):
        x = 0

        if len(self.indicators) > 0:
            for indicator in self.indicators.values():
                indicator.pack_forget()

            self.indicators.clear()

        for connection in list(self.main_frame.plc_data_connections.values()) :
            self.indicators[connection.plc.name] = Indicator(self.indicator_frame, connection.plc.name, RED)

        for indicator in self.indicators:
            self.indicators[indicator].pack(fill="x", padx=20)

            x += 1

    def toggle_indicator(self, state, plc_name):
        if len(self.indicators) > 0:

            try:
                if state:
                    self.indicators[plc_name].set_state(True)
                else:
                    self.indicators[plc_name].set_state(False)
            except KeyError:
                print(f"Key error for toggle indicator list: {self.indicators}")


    def output_alarm_message(self, message):
        self.alarm_output.add_message(message)

    def clear_alarm_messages(self):
        self.alarm_output.clear_messages()

