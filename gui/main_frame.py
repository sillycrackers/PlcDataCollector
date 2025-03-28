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
from utils import *


# Main Frame
class MainFrame(ttk.Frame):
    def __init__(self, root_window):
        super().__init__(master=root_window)

        self.root_window = root_window

        #Global Styles
        ttk.Style().configure('TLabelframe.Label', font=('Calibri', 13,))
        ttk.Style().configure('TButton', font=('Calibri', 12,))

        ttk.Style(theme='flatly')

        #Main Menu
        self.main_menu = MainMenu(root_window, self)
        self.root_window.configure(menu = self.main_menu)

        #Variables
        self.active_alarms = {}
        self.alarm_active = tk.BooleanVar()
        self.alarm_active.set(False)
        self.root_window = root_window
        self.plc_data_connections = {}

        self.halt_threads = False
        self.halt_threads_ack = False
        self.comm_thread_done = False
        self.read_thread_done = False

        self.file_loaded = False

        self.comm_lock = threading.Lock()
        self.read_lock = threading.Lock()

        self.threads = []
        self.q = Queue()
        self.root_window.bind("<<CheckQueue>>", self.process_queue)

        #Title
        self.title_frame = TitleFrame(self,text="PLC Data Collector",pady=50,padx=50)

        #Pack Self
        self.pack(expand=True, fill="both")

        #Body
        self.body_frame = BodyFrame(self)

    def open_manage_connections_window(self):

        manage_connections_toplevel = ManageConnectionsToplevel(root_window=self.root_window, parent_frame=self)

        manage_connections_frame = ManageConnectionsFrame(root_window=manage_connections_toplevel, connections=self.plc_data_connections, main_root_window=self.root_window)

        manage_connections_frame.pack()

    #Called by Tk.After function, this is what calls functions passed by the background threads
    def process_queue(self, event):
        """
        Read the queue
        """
        msg: Ticket
        msg = self.q.get()


        # ("message":str, Alarm active:bool)
        if msg.ticket_purpose == TicketPurpose.UPDATE_ALARMS:
            self.active_alarms[msg.ticket_value[0]] = msg.ticket_value[1]

        # (state:bool,"plc.name:str")
        if msg.ticket_purpose == TicketPurpose.TOGGLE_INDICATOR:
            self.body_frame.toggle_indicator(msg.ticket_value[0],msg.ticket_value[1])

        # Don't need argument passed for sg.value
        if msg.ticket_purpose == TicketPurpose.ACTIVE_ALARMS_CLEAR:
            self.active_alarms.clear()
            print("CLEAR")

        if msg.ticket_purpose == TicketPurpose.POPULATE_INDICATORS:
            self.body_frame.populate_indicators()
            print("POPULATE")

        self.q.task_done()



    #This method is being called by thread.
    def read_plc_data(self):
        print("reading tags")
        if len(self.plc_data_connections) > 0:
            self.read_lock.acquire()
            for connection in list(self.plc_data_connections.values()):
                connection.collect_data()
                if self.halt_threads:
                    break

            self.read_lock.release()

            self.read_thread_done = True


    def add_plc_connection(self, plc_connection):
        self.plc_data_connections[plc_connection.plc.name] = plc_connection

    # This method is being called by thread. It's checking the connection for all the plcs
    # and adding a tuple to the queue (name of the plc (str), True or False (connected or not))

    def check_connection(self):

        if len(self.plc_data_connections) > 0:

            self.comm_lock.acquire()
            for connection in self.plc_data_connections.values():
                print("Checking comms")
                if connection.check_plc_connection():

                    alarm_ticket = Ticket(ticket_purpose=TicketPurpose.UPDATE_ALARMS,
                                          ticket_value=(f"Lost Connection to {connection.plc.name}",False))
                    indicator_ticket = Ticket(ticket_purpose=TicketPurpose.TOGGLE_INDICATOR,
                                              ticket_value=(True, connection.plc.name))
                    self.q.put(alarm_ticket)
                    self.event_generate("<<CheckQueue>>")
                    self.q.put(indicator_ticket)
                    self.event_generate("<<CheckQueue>>")

                else:

                    alarm_ticket = Ticket(ticket_purpose=TicketPurpose.UPDATE_ALARMS,
                                          ticket_value=(f"Lost Connection to {connection.plc.name}",True))
                    indicator_ticket = Ticket(ticket_purpose=TicketPurpose.TOGGLE_INDICATOR,
                                              ticket_value=(False, connection.plc.name))
                    self.q.put(alarm_ticket)
                    self.event_generate("<<CheckQueue>>")
                    self.q.put(indicator_ticket)
                    self.event_generate("<<CheckQueue>>")

            self.comm_lock.release()

            self.comm_thread_done = True


    def refresh_active_alarms(self):

        self.threads.clear()

        self.body_frame.clear_alarm_messages()

        for alarm in self.active_alarms:
            if self.active_alarms[alarm]:
                self.body_frame.output_alarm_message(message=alarm)

        #Threads
        check_connection_thread = threading.Thread(target=self.check_connection, daemon=True)
        read_plc_data_thread = threading.Thread(target=self.read_plc_data, daemon=True)

        self.threads.append(check_connection_thread)
        self.threads.append(read_plc_data_thread)

        #Start the threads
        if not self.halt_threads and len(self.plc_data_connections) > 0:
            #print(f"Thread Done Values, comm thread done: {self.comm_thread_done} read thread done: {self.read_thread_done} Halt threads: {self.halt_threads} File Loaded: {self.file_loaded}")
            if self.comm_thread_done and self.read_thread_done or self.file_loaded:
                #print("Starting Threads")
                for thread in self.threads:
                    thread.start()
                self.file_loaded = False
                self.read_thread_done = False
                self.comm_thread_done = False

        self.after(250, self.refresh_active_alarms)

    def run_app(self):

        #Window thread that will clear list and show any active alarms
        self.after(100, self.refresh_active_alarms)

        self.mainloop()

