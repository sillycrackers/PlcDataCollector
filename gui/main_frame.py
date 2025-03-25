import tkinter as tk
import ttkbootstrap as ttk
from queue import Queue
import time
import threading

from gui.main_menu import MainMenu
from gui.title_frame import TitleFrame
from gui.body_frame import BodyFrame
from gui.manage_connections_frame import ManageConnectionsFrame
from gui.manage_connections_toplevel import ManageConnectionsToplevel


# Main Frame
class MainFrame(ttk.Frame):
    def __init__(self, root_window):
        super().__init__(master=root_window)

        self.root_window = root_window

        #Threads
        self.check_connection_thread = threading.Thread(target=self.check_connection, daemon=True)
        self.read_plc_data_thread = threading.Thread(target=self.read_plc_data, daemon=True)

        #Global Styles
        ttk.Style().configure('TLabelframe.Label', font=('Calibri', 13,))
        ttk.Style().configure('TButton', font=('Calibri', 12,))

        ttk.Style(theme='flatly')

        #Main Menu
        self.main_menu = MainMenu(root_window, self)
        self.root_window.configure(menu = self.main_menu)

        #Variables
        self.active_alarms = {}
        self.alarm_messages = []
        self.alarm_active = tk.BooleanVar()
        self.alarm_active.set(False)
        self.root_window = root_window
        self.plc_data_connections = {}

        self.q = Queue()

        #Title
        self.title_frame = TitleFrame(self,text="PLC Data Collector",pady=50,padx=50)

        self.toggle_button = ttk.Button(master=self, text="Toggle Indicators", command=self.toggle)
        self.toggle_button.pack()

        self.toggle_state = False

        #Pack Self
        self.pack(expand=True, fill="both")

        #Body
        self.body_frame = BodyFrame(self)


    def toggle(self):
        self.body_frame.toggle_indicator(self.toggle_state, "Plc 1")
        self.toggle_state = not self.toggle_state
        print(self.toggle_state)

    def open_manage_connections_window(self):

        manage_connections_toplevel = ManageConnectionsToplevel(root_window=self.root_window, parent_frame=self)

        manage_connections_frame = ManageConnectionsFrame(root_window=manage_connections_toplevel, connections=self.plc_data_connections)

        manage_connections_frame.pack()

    #Called by Tk.After function, this is what calls functions passed by the background threads
    def process_queue(self):

        if not self.q.empty():
            while not self.q.empty():
                self.q.get()
            self.q.task_done()

        # Schedule the next queue check
        self.after(50, self.process_queue)

    #This method is being called by thread.
    def read_plc_data(self):

        while True:
            while len(list(self.plc_data_connections)) > 0:
                for connection in list(self.plc_data_connections.values()):

                    result = connection.collect_data()

                    if result is None:
                        break
                    elif result[0]:
                        print("Collected Data")
                        self.q.put(self.update_alarms(result[1], False))
                    elif not result[0]:
                        self.q.put(self.update_alarms(result[1], True))


            time.sleep(0.1)

    def add_plc_connection(self, plc_connection):
        self.plc_data_connections[plc_connection.plc.name] = plc_connection

    # This method is being called by thread. It's checking the connection for all the plcs
    # and adding a tuple to the queue (name of the plc (str), True or False (connected or not))
    # We copy the dictionary values to a list to avoid accessing data that we could change when editing connection
    def check_connection(self):

        while True:
            while len(list(self.plc_data_connections)) > 0:
                for connection in list(self.plc_data_connections.values()):
                    if connection.check_plc_connection():
                        self.q.put(self.update_alarms(f"Lost connection to {connection.plc.name}",False))
                        self.q.put(self.body_frame.toggle_indicator(state=True, plc_name=connection.plc.name))
                        time.sleep(0.1)
                    else:
                        self.q.put(self.update_alarms(f"Lost connection to {connection.plc.name}",True))
                        self.q.put(self.body_frame.toggle_indicator(state=False, plc_name=connection.plc.name))
                        time.sleep(0.1)

            time.sleep(0.1)

    def update_alarms(self, message, state):
        self.active_alarms[message] = state

    def refresh_active_alarms(self):
        self.body_frame.clear_messages()

        for alarm in self.active_alarms:
            if self.active_alarms[alarm]:
                self.body_frame.output_message(message=alarm)

        self.after(250, self.refresh_active_alarms)

    def run_app(self):

        self.read_plc_data_thread.start()
        self.check_connection_thread.start()

        #Window thread that will process functions sent by background threads
        self.after(50, self.process_queue)
        #Window thread that will clear list and show any active alarms
        self.after(100, self.refresh_active_alarms)

        self.mainloop()

