import time
from json import JSONEncoder
from tkinter import filedialog
import json
import threading

from src.gui.about_window import AboutWindow
from src.plc_connection import PlcConnection, Plc, WriteType
from src.utils import *
from src.file_management import *

class PlcObjectEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class MainMenu(ttk.Menu):
    def __init__(self, parent_window, main_frame):
        super().__init__(master=parent_window)

        self.parent_window = parent_window
        self.main_frame = main_frame
        self.file_path = ''


        #File Menu
        self.file_menu = ttk.Menu(self,font="calibri 12")
        self.file_menu.add_command(label = "Open    ", command=lambda :self.create_open_file_thread("",False))
        self.file_menu.add_command(label="Save   ", command=self.save_file)
        self.file_menu.add_command(label="Save As   ", command=self.save_file_as)
        #self.file_menu.add_separator()
        self.add_cascade(label="  File  ",menu= self.file_menu)

        #View Menu
        self.view_menu = ttk.Menu(self, font="calibri 12")
        self.add_cascade(label="  View  ",menu=self.view_menu)
        #Theme Sub Menu
        self.theme_menu = ttk.Menu(self.view_menu, font="calibri 12")
        self.theme_menu.add_command(label="Dark Theme", command=lambda : self.change_theme('dark'))
        self.theme_menu.add_command(label="Light Theme", command=lambda : self.change_theme('light'))
        self.view_menu.add_cascade(label="  Theme  ", menu=self.theme_menu)

        #Help Menu
        self.help_menu = ttk.Menu(self, font='calibri 12')
        self.help_menu.add_command(label="About    ", command=self.open_about)
        self.add_cascade(label="  Help  ", menu=self.help_menu)

    def open_about(self):

        about_window = AboutWindow(self.parent_window)

    def change_theme(self, theme):
        change_theme(theme)

    def decode_json_to_plc_objects(self, json_string):

        json_dict = json.loads(json_string)

        plcs = []

        for plc in json_dict:
            newPlc = Plc()

            newPlc.name = plc['name']
            newPlc.ip_address = plc['ip_address']
            newPlc.trigger_tag = plc['trigger_tag']
            newPlc.ack_tag = plc['ack_tag']
            newPlc.tags = plc['tags']
            newPlc.excel_file_name = plc['excel_file_name']
            newPlc.excel_file_location = plc['excel_file_location']
            newPlc.file_path = plc['file_path']
            newPlc.write_type = plc['write_type']

            plcs.append(newPlc)

        return plcs

    def create_open_file_thread(self, file_path, booting):
        open_file_thread = threading.Thread(daemon=True, target=self.open_file,args=(file_path, booting) )

        open_file_thread.start()

    def open_file(self,file_path="", booting=False):

        if not booting:
            file_path = filedialog.askopenfilename(defaultextension=".pdc", filetypes=[("PLC Data Collector",'*.pdc')])
        else:
            booting = False

        if os.path.exists(file_path):

            self.main_frame.halt_threads = True

            transmit(self.main_frame, Ticket(purpose=TicketPurpose.SHOW_WAIT_CURSOR, value=self.parent_window))
            transmit(self.main_frame, Ticket(purpose=TicketPurpose.SHOW_ANIMATED_LABEL, value=self.main_frame.loading_label))

            if len(self.main_frame.plc_data_connections) > 0:
                while self.main_frame.comm_thread_done == False or self.main_frame.read_thread_done == False:
                    print("waiting")
                    print(f"comm thread done: {self.main_frame.comm_thread_done} read thread done: {self.main_frame.read_thread_done }")
                    time.sleep(0.5)

            with open(file_path, 'r') as file:
                file_content = file.read()

            self.main_frame.read_lock.acquire()
            self.main_frame.comm_lock.acquire()

            self.main_frame.plc_data_connections.clear()

            for plc in self.decode_json_to_plc_objects(file_content):
                self.main_frame.add_plc_connection(PlcConnection(plc, self.main_frame))

            self.main_frame.comm_lock.release()
            self.main_frame.read_lock.release()

            print("NEW FILE!")

            transmit(self.main_frame,Ticket(purpose=TicketPurpose.ACTIVE_ALARMS_CLEAR, value=None))
            transmit(self.main_frame,Ticket(purpose=TicketPurpose.POPULATE_INDICATORS, value=None))
            transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_NORMAL_CURSOR, value=self.parent_window))
            transmit(self.main_frame,Ticket(purpose=TicketPurpose.HIDE_ANIMATED_LABEL,
                                          value=self.main_frame.loading_label))

            self.main_frame.file_loaded = True
            self.main_frame.halt_threads = False

            set_reg(file_path)
            self.file_path = file_path


    def save_file_as(self):

        #print(json_string)

        files = [("PLC Data Collector",'*.pdc')]

        try:

            self.file_path = filedialog.asksaveasfilename(filetypes=files)

            if not self.file_path.endswith(".pdc"):
                self.file_path += ".pdc"

            self.main_frame.data_changed = False

        except Exception:

            print("Error while saving file")

    def save_file(self):


        if self.file_path:
            plc_list = []

            for item in list(self.main_frame.plc_data_connections.values()):
                plc_list.append(item.plc)

            json_string = json.dumps(obj=plc_list, cls=PlcObjectEncoder)

            f = open(self.file_path, "w")
            f.write(json_string)
            f.close()

            set_reg(self.file_path)

        else:
            print("No file path to save to. Use: 'Save As'")
