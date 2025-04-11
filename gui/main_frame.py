import tkinter as tk
from queue import Queue
import threading
from datetime import datetime

from gui.main_menu import MainMenu
from gui.title_frame import TitleFrame
from gui.left_body_frame import LeftBodyFrame
from gui.manage_connections_toplevel import ManageConnectionsToplevel
from utils import *
from gui.animated_label import AnimatedLabel
from gui.right_body_frame import RightBodyFrame
from gui.collecting_data_frame import CollectingDataFrame
from ticketing_system import *
from file_management import *


# Main Frame
class MainFrame(tk.Frame):
    def __init__(self, root_window):
        super().__init__(master=root_window)

        self.root_window = root_window

        #change_theme("dark")

        #Pack Self
        self.pack(expand=True, fill="both")

        #Main Menu
        self.main_menu = MainMenu(root_window, self)
        self.root_window.configure(menu = self.main_menu)

        #Variables
        self.active_alarms = {}
        self.alarm_active = tk.BooleanVar()
        self.alarm_active.set(False)
        self.root_window = root_window
        self.plc_data_connections = {}
        self.dot_count = 1
        self.show_loading_animation = False
        self.halt_threads = False
        self.halt_threads_ack = False
        self.comm_thread_done = True
        self.read_thread_done = True
        self.file_loaded = False
        self.click_count = 0
        self.comm_lock = threading.Lock()
        self.read_lock = threading.Lock()
        self.threads = []
        self.q = Queue()
        self.ticketer = TicketingSystem(self)

        #========== Window Events ==============#

        self.root_window.bind("<<CheckQueue>>", self.process_queue)
        self.root_window.bind("<Button>", self.on_mouse_click)
        self.root_window.bind("<Control-e>", self.on_key_press)

        #===============Widgets================#

        # =========Top Frame==========#
        #-----------------------------#
        self.top_frame = ttk.Frame(self)

        #======== Wrapper Frame (Wrap everything inside Top Frame) ======#
        self.top_frame_wrapper = ttk.Frame(self.top_frame)
        #Title Frame
        self.title_frame = TitleFrame(self.top_frame_wrapper, text="PLC Data Collector")

        #Inner Top Frame (contents below Title Frame)
        self.inner_top_frame = ttk.Frame(self.top_frame_wrapper)
        #Collecting data frame
        self.collecting_data_frame = CollectingDataFrame(self.inner_top_frame)
        #Loading label frame
        self.loading_label_frame = ttk.Frame(self.inner_top_frame)

        #Button for testing purposes
        self.test_button = ttk.Button(self.top_frame_wrapper, text="Test", width=15, name="test_button",
                                      command=lambda : self.on_button_press("test_button"))


        #Loading Label
        self.loading_label = AnimatedLabel(self.loading_label_frame, text="Loading")
        self.loading_label.pack()

        #==== Pack to Inner Top Frame ====#
        self.collecting_data_frame.pack(side="left")
        self.loading_label_frame.pack(side="left")

        #==== Pack frames into Top Frame Wrapper ====#
        self.title_frame.pack()
        self.inner_top_frame.pack(side="left")
        self.test_button.pack(side="bottom")

        #==== Pack Top Frame Wrapper to Top Frame =====#
        self.top_frame_wrapper.pack(side="left")


        #=========Main Body Frame==========#
        #----------------------------------#
        self.main_body_frame = ttk.Frame(self)
        #Left Body Frame
        self.left_body_frame = LeftBodyFrame(parent_frame=self.main_body_frame,main_frame=self)
        #Right Body Frame
        self.right_body_frame = RightBodyFrame(parent_frame=self.main_body_frame, main_frame=self)

        #==== Pack Widgets on Frame ====#
        self.left_body_frame.pack(side="left", fill="y", pady=(20,20), padx=(20,10))
        self.right_body_frame.pack(side="right", expand=True, fill="both", pady=(20,20), padx=(0,20))

        #===============Main Layout================#
        #------------------------------------------#
        self.top_frame.pack(fill='x', padx=(20,0), pady=(20,0))
        self.main_body_frame.pack(expand=True, fill="both")

    def after_rotate_image(self):

        if not self.halt_threads:
            self.collecting_data_frame.rotate()

        self.after(10, self.after_rotate_image)
    #Function called when mouse is clicked anywhere
    def on_mouse_click(self, var):

        #Unselect item in treeview
        if len(self.right_body_frame.output.listbox.selection()) > 0:
            self.right_body_frame.output.listbox.selection_remove(self.right_body_frame.output.listbox.selection()[0])

    def on_button_press(self, *args):

        data_row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "test", "data", "this"]

        if args:
            if args[0] == "test_button":
               save_data_to_excel(header=["data1","data2","data3"],data=data_row ,file_path="C:\\Users\\silly\\OneDrive\\Documents\\Python\\test_data.xlsx",sheet_name= "Test Data")

    #Called by Tk.After function, this is what calls functions passed by the background threads
    def process_queue(self, event):
        """
        Read the queue
        """
        msg: Ticket
        msg = self.q.get()

        match msg.purpose:

            case TicketPurpose.UPDATE_ALARMS:
                # ("message":str, Alarm active:bool)
                self.active_alarms[msg.value[0]] = msg.value[1]

            case TicketPurpose.TOGGLE_INDICATOR:
                # (state:bool,"plc.name:str")
                self.left_body_frame.toggle_indicator(msg.value[0], msg.value[1])

            case TicketPurpose.ACTIVE_ALARMS_CLEAR:
                self.active_alarms.clear()

            case TicketPurpose.POPULATE_INDICATORS:
                self.left_body_frame.populate_indicators()

            case TicketPurpose.SHOW_WAIT_CURSOR:
                # (window:ttk.Window)
                msg.value.config(cursor="watch")
                msg.value.update_idletasks()
                self.freeze_window(msg.value)

            case TicketPurpose.SHOW_NORMAL_CURSOR:
                # window:ttk.Window
                msg.value.config(cursor="")
                msg.value.update_idletasks()
                self.unfreeze_window(msg.value)

            case TicketPurpose.SHOW_ANIMATED_LABEL:
                # (AnimatedLabel: object)
                msg.value.pack()
                self.show_loading_animation = True
                self.after(100, self.label_animation, msg.value)

            case TicketPurpose.HIDE_ANIMATED_LABEL:
                self.show_loading_animation = False
                msg.value.pack_forget()

                # message : str
            case TicketPurpose.OUTPUT_MESSAGE:
                self.output_message(msg.value)

        self.q.task_done()

    def on_key_press(self, event):

        self.root_window.destroy()

        #"Application closed with Ctrl-e"

        sys.exit("Application closed with Ctrl-e")

        #Ctrl + c to quit program
        #<KeyPress event send_event=True state=Control|Mod1 keysym=c keycode=67 char='\x03' x=165 y=27>

    #This method is being called by thread.
    def read_plc_data(self):
        if len(self.plc_data_connections) > 0:
            self.read_lock.acquire()
            for connection in self.plc_data_connections.values():
                connection.collect_data()
                if self.halt_threads:
                    break

            self.read_lock.release()

        self.read_thread_done = True

    def label_animation(self, label):

        if self.show_loading_animation:

            label.adjust_dots()

            self.after(400, self.label_animation, label)

    def open_manage_connections_window(self):

        manage_connections_toplevel = ManageConnectionsToplevel(root_window=self.root_window, main_frame=self)

    def add_plc_connection(self, plc_connection):
        self.plc_data_connections[plc_connection.plc.name] = plc_connection

    # This method is being called by thread. It's checking the connection for all the plcs
    # and adding a tuple to the queue (name of the plc (str), True or False (connected or not))

    def check_connection(self):

        if len(self.plc_data_connections) > 0:

            self.comm_lock.acquire()
            for connection in self.plc_data_connections.values():
                if connection.check_plc_connection():

                    self.ticketer.transmit(Ticket(purpose=TicketPurpose.UPDATE_ALARMS, value=(f"Lost Connection to {connection.plc.name}", False)))
                    self.ticketer.transmit(Ticket(purpose=TicketPurpose.TOGGLE_INDICATOR, value=(True, connection.plc.name)))

                else:

                    self.ticketer.transmit(Ticket(purpose=TicketPurpose.UPDATE_ALARMS, value=(f"Lost Connection to {connection.plc.name}", True)))
                    self.ticketer.transmit(Ticket(purpose=TicketPurpose.TOGGLE_INDICATOR, value=(False, connection.plc.name)))

            self.comm_lock.release()

        self.comm_thread_done = True

    def after_refresh_active_alarms(self):


        self.threads.clear()

        self.left_body_frame.clear_alarm_messages()

        for alarm in self.active_alarms:
            if self.active_alarms[alarm]:
                self.left_body_frame.output_alarm_message(message=alarm)

        #Thread
        if self.comm_thread_done and self.read_thread_done or self.file_loaded:
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

        self.after(250, self.after_refresh_active_alarms)

    def freeze_window(self, window):
        window.attributes('-disabled', 1)

    def unfreeze_window(self, window):
        window.attributes('-disabled', 0)

    def output_message(self, message):

        self.right_body_frame.output.add_message(message)

    def run_app(self):

        #Window thread that will clear list and show any active alarms
        self.after(100, self.after_refresh_active_alarms)

        self.after(1000, self.after_rotate_image)

        fp = get_reg(r"SOFTWARE\\Plc Data Collector\\")

        try:
            if fp:
                self.main_menu.create_open_file_thread(fp,True)
        except Exception:
            print("Error, Didn't load file, cannot find last file loaded")

        self.left_body_frame.populate_indicators()

        self.mainloop()

