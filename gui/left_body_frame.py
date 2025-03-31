import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import *

from gui.new_output_display import NewOutputDisplay
from gui.output_display import OutputDisplay
from gui.indicator import Indicator
from gui.colors import *


class LeftBodyFrame(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(master=main_frame)

        self.main_frame = main_frame



        self.indicators = {}

        self.title_label = ttk.Label(self, text="PLC Connections", font="calibri 14", justify="left")
        self.title_label.pack(fill='x')

        self.border_frame = ttk.Frame(self, borderwidth=1, relief=tk.RIDGE)
        self.border_frame.pack(fill="both", expand=True)

        self.indicator_frame = ScrolledFrame(self.border_frame)
        self.indicator_frame.pack(fill="both", expand=True)

        self.indicator_frame.columnconfigure(index=0, weight=1)
        self.indicator_frame.columnconfigure(index=1, weight=1)
        self.indicator_frame.columnconfigure(index=2, weight=2)
        self.indicator_frame.rowconfigure(index=(0, 1, 2), weight=1)

        self.spacer_label1 = ttk.Label(self.indicator_frame)
        self.spacer_label2 = ttk.Label(self.indicator_frame)

        self.spacer_label1.grid(row=0, column=0, sticky='ew')
        self.spacer_label2.grid(row=0,column=2, sticky='ew')

        self.open_manage_connections_button = ttk.Button(self,style='custom.TButton', text="Manage Connections", command=self.main_frame.open_manage_connections_window)
        self.open_manage_connections_button.pack(ipady=5, ipadx=5)

        self.alarm_title = ttk.Label(self, text="Active Alarms", font="calibri 14", foreground='red', justify="left")
        self.alarm_title.pack(fill="x")

        self.alarm_output = NewOutputDisplay(self, style='alarm.Treeview')
        self.alarm_output.pack()

    #Create and display indicators the indicators for all connections
    #First we clear the current displayed indicators and make a new dictionary of the required indicators
    #The reason for using a dictionary instead of a list is so we can toggle specific ones later
    def populate_indicators(self):
        x = 0

        if len(self.indicators) > 0:
            for indicator in self.indicators.values():
                indicator.grid_forget()

            self.indicators.clear()

        for connection in list(self.main_frame.plc_data_connections.values()) :
            self.indicators[connection.plc.name] = Indicator(self.indicator_frame, connection.plc.name, RED)

        for indicator in self.indicators:
            self.indicators[indicator].grid(row=x, column=1, sticky='nse')

            x += 1

    def toggle_indicator(self, state, plc_name):
        if len(self.indicators) > 0:
            if state:
                self.indicators[plc_name].set_state(True)
            else:
                self.indicators[plc_name].set_state(False)


    def output_alarm_message(self, message):
        self.alarm_output.add_message(message)


    def clear_alarm_messages(self):
        self.alarm_output.clear_messages()

