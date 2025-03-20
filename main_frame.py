import tkinter as tk
import ttkbootstrap as ttk
from queue import Queue
import time
import threading


from main_menu import MainMenu
from title_frame import TitleFrame
from body_frame import BodyFrame
from manage_connections_window import ManageConnectionsWindow
from colors import *
from fonts import *

'''
dark themes: solar, superhero, darkly, cyborg, vapor
light themes: cosmo, flatly, journal, litera, lumen, minty, pulse, sandstone, united, yeti, morph, simplex, cerculean, 
'''

# Main Frame
class MainFrame(ttk.Frame):
    def __init__(self, root_window):
        super().__init__(master=root_window)

        self.root_window = root_window

        #Threads
        self.check_connection_thread = threading.Thread(target=self.check_connection, daemon=True)
        self.read_plc_data_thread = threading.Thread(target=self.read_plc_data, daemon=True)

        #Thread list
        self.threads = [self.check_connection_thread, self.read_plc_data_thread]

        #Global Styles
        ttk.Style().configure('TLabelframe.Label', font=('Calibri', 13,))
        ttk.Style().configure('TButton', font=('Calibri', 12,))

        ttk.Style(theme='flatly')

        #Main Menu
        self.main_menu = MainMenu(root_window, self)
        self.root_window.configure(menu = self.main_menu)

        #Variables
        self.plc_data_connections = {}
        self.active_alarms = {}
        self.alarm_messages = []
        self.alarm_active = tk.BooleanVar()
        self.alarm_active.set(False)
        self.root_window = root_window

        self.q = Queue()

        #Title
        self.title_frame = TitleFrame(self,text="PLC Data Collector",pady=50,padx=50)

        #Body
        self.body_frame = BodyFrame(self)

        #Pack Self
        self.pack(expand=True, fill="both")

    def open_manage_connections_window(self):

        manage_connections = ManageConnectionsWindow(root_window=self.root_window, plc_data_connections=self.plc_data_connections, parent=self)

    def add_plc_connection(self, plc_connection):
        self.plc_data_connections[plc_connection.plc.name] = plc_connection

    def replace_plc_connection(self, new_plc_connection, old_plc_connection):

        self.plc_data_connections.pop(old_plc_connection.plc.name)
        self.plc_data_connections[new_plc_connection.plc.name]=new_plc_connection

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
                    connection.collect_data()

            time.sleep(0.1)

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

        self.after(1000, self.refresh_active_alarms)

    def change_theme(self, theme):

        if theme == 'dark':
            ttk.Style(theme='darkly')
        elif theme == 'light':
            ttk.Style(theme='flatly')

    def run_app(self):


        #flash_indicator_thread1 = threading.Thread(target=self.flash_indicator, args=(self.body_frame.indicators[0], 0.1), daemon=True)
        #flash_indicator_thread2 = threading.Thread(target=self.flash_indicator, args=(self.body_frame.indicators[1], 0.1), daemon=True)

        self.read_plc_data_thread.start()
        self.check_connection_thread.start()
        #flash_indicator_thread1.start()
        #time.sleep(0.05)
        #flash_indicator_thread2.start()

        self.after(50, self.process_queue)
        self.after(100, self.refresh_active_alarms)

        self.mainloop()

