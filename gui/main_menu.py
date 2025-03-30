import time
from json import JSONEncoder
import ttkbootstrap as ttk
from tkinter import filedialog
import json
import os
import threading

from gui.about_window import AboutWindow
from plc import Plc
from plc_connection import PlcConnection
from utils import *

class PlcObjectEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class MainMenu(ttk.Menu):
    def __init__(self, parent_window, parent):
        super().__init__(master=parent_window)

        self.parent_window = parent_window
        self.parent = parent

        #File Menu
        self.file_menu = ttk.Menu(self,font="calibri 12")
        self.file_menu.add_command(label = "Open",command=self.create_open_file_thread)
        self.file_menu.add_command(label="Save", command=self.save_file)
        #self.file_menu.add_separator()
        self.add_cascade(label="File",menu= self.file_menu)

        #View Menu
        self.view_menu = ttk.Menu(self, font="calibri 12")
        self.add_cascade(label="View",menu=self.view_menu)
        #Theme Sub Menu
        self.theme_menu = ttk.Menu(self.view_menu, font="calibri 12")
        self.theme_menu.add_command(label="Dark Theme", command=lambda : self.change_theme('dark'))
        self.theme_menu.add_command(label="Light Theme", command=lambda: self.change_theme('light'))
        self.view_menu.add_cascade(label="Theme", menu=self.theme_menu)

        #Help Menu
        self.help_menu = ttk.Menu(self, font='calibri 12')
        self.help_menu.add_command(label="About", command=self.open_about)
        self.add_cascade(label="Help", menu=self.help_menu)

    def open_about(self):

        about_window = AboutWindow(self.parent_window)

    def change_theme(self, theme):
        change_theme(theme)

    def decode_json_to_plc_objects(self, json_string):

        dict = json.loads(json_string)

        plcs = []

        for plc in dict:
            newPlc = Plc()

            newPlc.name = plc['name']
            newPlc.ip_address = plc['ip_address']
            newPlc.trigger_tag = plc['trigger_tag']
            newPlc.ack_tag = plc['ack_tag']
            newPlc.tags = plc['tags']
            newPlc.excel_file_name = plc['excel_file_name']
            newPlc.excel_file_location = plc['excel_file_location']
            newPlc.file_path = plc['file_path']

            plcs.append(newPlc)

        return plcs

    def create_open_file_thread(self):
        open_file_thread = threading.Thread(target=self.open_file, daemon=True)

        open_file_thread.start()


    def open_file(self):

        file_path = filedialog.askopenfilename(defaultextension=".pdc", filetypes=[("PLC Data Collector",'*.pdc')])

        if os.path.exists(file_path):

            self.parent.halt_threads = True


            wait_cursor_ticket = Ticket(ticket_purpose=TicketPurpose.SHOW_WAIT_CURSOR, ticket_value=None)
            self.parent.q.put(wait_cursor_ticket)
            self.parent.event_generate("<<CheckQueue>>")

            if len(self.parent.plc_data_connections) > 0:
                while self.parent.comm_thread_done == False or self.parent.read_thread_done == False:
                    print("waiting")
                    print(f"comm thread done: {self.parent.comm_thread_done} read thread done: {self.parent.read_thread_done }")
                    time.sleep(0.5)

            with open(file_path, 'r') as file:
                file_content = file.read()

            self.parent.read_lock.acquire()
            self.parent.comm_lock.acquire()

            self.parent.plc_data_connections.clear()

            for plc in self.decode_json_to_plc_objects(file_content):
                self.parent.add_plc_connection(PlcConnection(plc,self.parent.halt_threads))

            self.parent.comm_lock.release()
            self.parent.read_lock.release()

            print("NEW FILE!")


            active_alarm_clear_ticket = Ticket(ticket_purpose=TicketPurpose.ACTIVE_ALARMS_CLEAR,ticket_value=None)
            populate_indicators_ticket = Ticket(ticket_purpose=TicketPurpose.POPULATE_INDICATORS, ticket_value=None)
            normal_cursor_ticket = Ticket(ticket_purpose=TicketPurpose.SHOW_NORMAL_CURSOR, ticket_value=None)

            self.parent.q.put(active_alarm_clear_ticket)
            self.parent.event_generate("<<CheckQueue>>")
            self.parent.q.put(populate_indicators_ticket)
            self.parent.event_generate("<<CheckQueue>>")
            self.parent.q.put(normal_cursor_ticket)
            self.parent.event_generate("<<CheckQueue>>")


            self.parent.file_loaded = True
            self.parent.halt_threads = False


    def save_file(self):

        plc_list = []

        for item in list(self.parent.plc_data_connections.values()):
            plc_list.append(item.plc)

        json_string = json.dumps(plc_list, cls=PlcObjectEncoder)


        files = [("PLC Data Collector",'*.pdc')]

        file_path = filedialog.asksaveasfilename(filetypes=files)

        if not file_path.endswith(".pdc"):
            file_path += ".pdc"

        f = open(file_path, "w")
        f.write(json_string)
        f.close()

