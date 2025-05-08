import time
from json import JSONEncoder
from tkinter import filedialog
import json
import threading
import subprocess

from src.gui.about_window import AboutWindow
from src.plc_connection import PlcConnection, Plc, WriteType
from src.utils import *
from src.file_management import *
import src.ticketing_system as ts
from src.gui.manual_top_level import ManualTopLevel


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
        self.help_menu.add_command(label="Manual    ", command=self.open_manual)
        self.add_cascade(label="  Help  ", menu=self.help_menu)

    def open_manual(self):

        subprocess.Popen([resource_path("src\\PLC Data Collector Manual.pdf")], shell=True)

    def open_about(self):

        about_window = AboutWindow(self.parent_window, self.main_frame)

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

            try:
                newPlc.write_type = plc['write_type']
            except KeyError:
                print(f"File being loaded is missing 'write_type' for {plc['name']}, may be an old version")
                newPlc.write_type = WriteType.APPEND

            plcs.append(newPlc)

        return plcs

    def create_open_file_thread(self, file_path, booting):
        open_file_thread = threading.Thread(daemon=True, target=self.open_file,args=(file_path, booting) )

        open_file_thread.start()

    def open_file(self,file_path="", booting=False):

        if not booting:
            file_path = filedialog.askopenfilename(defaultextension=".pdc", filetypes=[("PLC Data Collector",'*.pdc')])
            self.obtain_data_control()

        if os.path.exists(file_path):

            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()


                self.main_frame.plc_data_connections.clear()

                for plc in self.decode_json_to_plc_objects(file_content):
                    (self.main_frame.
                     add_plc_connection(PlcConnection(plc, self.main_frame)))

                self.release_data_control()

                self.main_frame.file_loaded = True
                booting = False

                set_reg(file_path)
                self.file_path = file_path

                self.parent_window.title(f"PLC Data Collector {self.main_frame.version}      File Loaded:   {file_path}")

            except Exception:
                print("Error trying to open file")

                self.release_data_control()

                self.main_frame.file_loaded = True

        else:
            print(f"File path doesn't exist")

    def obtain_data_control(self):

        self.main_frame.halt_threads = True

        transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_WAIT_CURSOR, value=self.parent_window))
        transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_ANIMATED_LABEL, value=self.main_frame.loading_label))

        while self.main_frame.threads_done != True:
            time.sleep(.1)

    def release_data_control(self):
        self.main_frame.file_loaded = True
        self.main_frame.halt_threads = False
        self.main_frame.threads_done = False

        transmit(self.main_frame, Ticket(purpose=TicketPurpose.ACTIVE_ALARMS_CLEAR, value=None))
        transmit(self.main_frame, Ticket(purpose=TicketPurpose.POPULATE_INDICATORS, value=None))
        transmit(self.main_frame, Ticket(purpose=TicketPurpose.SHOW_NORMAL_CURSOR, value=self.parent_window))
        transmit(self.main_frame, Ticket(purpose=TicketPurpose.HIDE_ANIMATED_LABEL, value=self.main_frame.loading_label))

    def save_file_as(self):


        files = [("PLC Data Collector",'*.pdc')]

        try:

            self.file_path = filedialog.asksaveasfilename(filetypes=files)

            if not self.file_path.endswith(".pdc"):
                self.file_path += ".pdc"

            self.main_frame.data_changed = False

            self.save_file()

        except Exception:

            print("Error while saving file")

    def save_file(self):


        if self.file_path:
            plc_list = []

            self.obtain_data_control()

            for item in list(self.main_frame.plc_data_connections.values()):
                plc_list.append(item.plc)

            json_string = json.dumps(obj=plc_list, cls=PlcObjectEncoder)

            f = open(self.file_path, "w")
            f.write(json_string)
            f.close()

            set_reg(self.file_path)

            ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.OUTPUT_MESSAGE,
                                                   value=f"File saved to : {self.file_path}"))

            self.release_data_control()

        else:
            print("No file path to save to. Use: 'Save As'")
