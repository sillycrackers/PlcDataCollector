import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import *

from gui.output_display import OutputDisplay
from gui.indicator import Indicator
from gui.colors import *

class BodyFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)

        self.parent = parent

        self.indicators = {}

        #Body
        self.pack(side="top", fill="x", pady=(0, 10), padx=10)

        #PLC Indicator List
        self.indicator_label_frame = ttk.LabelFrame(self,text="Connections")
        self.indicator_label_frame.pack(side="top",fill="x", pady=10)

        self.inside_frame = ScrolledFrame(self.indicator_label_frame)
        self.inside_frame.pack(fill="both",expand=True)

        self.inside_frame.columnconfigure(index=0,weight=1)
        self.inside_frame.columnconfigure(index=1, weight=1)
        self.inside_frame.columnconfigure(index=2, weight=2)
        self.inside_frame.rowconfigure(index=(0,1,2), weight=1)

        self.spacer_label1 = ttk.Label(self.inside_frame)
        self.spacer_label2 = ttk.Label(self.inside_frame)

        self.spacer_label1.grid(row=0, column=0, sticky='ew')
        self.spacer_label2.grid(row=0,column=2, sticky='ew')

        self.open_manage_connections_button = ttk.Button(self, text="Manage Connections", command=parent.open_manage_connections_window)
        self.open_manage_connections_button.pack(ipady=5, ipadx=5)

        self.alarm_title = ttk.Label(self, text="Active Alarms", font="calibri 16", foreground='red')
        self.alarm_title.pack(pady=(20,0))

        self.output = OutputDisplay(self)
        self.output.pack()

    #Create and display indicators the indicators for all connections
    #First we clear the current displayed indicators and make a new dictionary of the required indicators
    #The reason for using a dictionary instead of a list is so we can toggle specific ones later
    def populate_indicators(self):
        x = 0

        if len(self.indicators) > 0:
            for indicator in self.indicators.values():
                indicator.grid_forget()

            self.indicators.clear()

        for connection in list(self.parent.plc_data_connections.values()) :
            self.indicators[connection.plc.name] = Indicator(self, connection.plc.name, RED)

        for indicator in self.indicators:
            self.indicators[indicator].grid(row=x, column=1, sticky='nse')
            print(indicator)
            x += 1

    def toggle_indicator(self, state, plc_name):

        if state:
            self.indicators[plc_name].set_color(GREEN)
        else:
            self.indicators[plc_name].set_color(RED)

    def output_message(self, message):
        self.output.add_message(message)
        self.output.listbox.see(tk.END)  # Auto-scroll to the latest message

    def clear_messages(self):
        self.output.clear_messages()

