import ttkbootstrap as ttk
import tkinter as tk
from queue import Queue
import threading
import sys

from src.worker_thread import WorkerThread
from src.gui.main_menu import MainMenu
from src.gui.title_frame import TitleFrame
from src.gui.left_body_frame import LeftBodyFrame
from src.gui.manage_connections_toplevel import ManageConnectionsToplevel
from src.gui.animated_label import AnimatedLabel
from src.gui.right_body_frame import RightBodyFrame
from src.gui.collecting_data_frame import CollectingDataFrame
from src.utils import change_theme
import src.ticketing_system as ts
import src.file_management as fm
from src.thread_manager import ThreadManager


# Main Frame
class MainFrame(ttk.Frame):
    def __init__(self, root_window):
        super().__init__(master=root_window)

        self.root_window = root_window

        change_theme("dark")

        #Pack Self
        self.pack(expand=True, fill="both")

        #Variables
        self.version = "2.3"
        self.active_alarms = {}
        self.root_window = root_window
        self.plc_data_connections = {}
        self.dot_count = 1
        self.show_loading_animation = False
        self.file_loaded = False

        self.q = Queue()

        self.thread_manager = ThreadManager(self.plc_data_connections)

        self.root_window.title(f"PLC Data Collector {self.version}")

        #Main Menu
        self.main_menu = MainMenu(root_window, self)
        self.root_window.configure(menu = self.main_menu)

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

        #Loading Label
        self.loading_label = AnimatedLabel(self.loading_label_frame, text="Loading")
        self.loading_label.pack()

        #==== Pack to Inner Top Frame ====#
        self.collecting_data_frame.pack(side="left")
        self.loading_label_frame.pack(side="left")

        #==== Pack frames into Top Frame Wrapper ====#
        self.title_frame.pack()
        self.inner_top_frame.pack(side="left")

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
        self.left_body_frame.pack(side="left", fill="y", pady=(26,20), padx=(20,10))
        self.right_body_frame.pack(side="right", expand=True, fill="both", pady=(20,20), padx=(0,20))

        #===============Main Layout================#
        #------------------------------------------#
        self.top_frame.pack(fill='x', padx=(20,0), pady=(20,0))
        self.main_body_frame.pack(expand=True, fill="both")

    def after_rotate_image(self):

        if not self.thread_manager.halt_threads and len(self.plc_data_connections) > 0:
            self.collecting_data_frame.rotate()

        self.after(10, self.after_rotate_image)
    #Function called when mouse is clicked anywhere
    def on_mouse_click(self, var):
        #Unselect item in treeview
        if len(self.right_body_frame.output.listbox.selection()) > 0:
            self.right_body_frame.output.listbox.selection_remove(self.right_body_frame.output.listbox.selection()[0])

    #Called by Tk.After function, this is what calls functions passed by the background threads
    def process_queue(self, event):
        """
        Read the queue
        """
        msg: ts.Ticket
        msg = self.q.get()

        match msg.purpose:

            case ts.TicketPurpose.UPDATE_ALARMS:
                # ("message":str, Alarm active:bool)
                self.active_alarms[msg.value[0]] = msg.value[1]

            case ts.TicketPurpose.TOGGLE_INDICATOR:
                # (state:bool,"plc.name:str")
                self.left_body_frame.toggle_indicator(msg.value[0], msg.value[1])

            case ts.TicketPurpose.ACTIVE_ALARMS_CLEAR:
                self.active_alarms.clear()

            case ts.TicketPurpose.POPULATE_INDICATORS:
                self.left_body_frame.populate_indicators()

            case ts.TicketPurpose.SHOW_WAIT_CURSOR:
                # (window:ttk.Window)
                msg.value.config(cursor="watch")
                msg.value.update_idletasks()
                self.freeze_window(msg.value)

            case ts.TicketPurpose.SHOW_NORMAL_CURSOR:
                # window:ttk.Window
                msg.value.config(cursor="")
                msg.value.update_idletasks()
                self.unfreeze_window(msg.value)

            case ts.TicketPurpose.SHOW_ANIMATED_LABEL:
                # (AnimatedLabel: object)
                msg.value.pack()
                self.show_loading_animation = True
                self.after(100, self.label_animation, msg.value)

            case ts.TicketPurpose.HIDE_ANIMATED_LABEL:
                self.show_loading_animation = False
                msg.value.pack_forget()

                # message : str
            case ts.TicketPurpose.OUTPUT_MESSAGE:
                self.output_message(msg.value)

            case _:
                print(f"Unhandled ticket purpose: {msg.purpose}")

        self.q.task_done()

    def on_key_press(self, event):

        self.root_window.destroy()

        #"Application closed with Ctrl-e"

        sys.exit("Application closed with Ctrl-e")

    def label_animation(self, label):

        if self.show_loading_animation:

            label.adjust_dots()

            self.after(400, self.label_animation, label)

    def open_manage_connections_window(self):

        manage_connections_toplevel = ManageConnectionsToplevel(root_window=self.root_window, main_frame=self)

    def add_plc_connection(self, plc_connection):
        self.plc_data_connections[plc_connection.plc.name] = plc_connection

    def delete_plc_connection(self, plc_name):
        del self.plc_data_connections[plc_name]

    # This method is being called by thread. It's checking the connection for the plc
    # and adding a tuple to the queue (name of the plc (str), True or False (connected or not))

    def after_refresh_active_alarms(self):

        self.left_body_frame.clear_alarm_messages()

        for alarm in self.active_alarms:
            if self.active_alarms[alarm]:
                self.left_body_frame.output_alarm_message(message=alarm)

        self.after(10, self.after_refresh_active_alarms)

    def freeze_window(self, window):
        window.attributes('-disabled', 1)

    def unfreeze_window(self, window):
        window.attributes('-disabled', 0)

    def output_message(self, message):

        self.right_body_frame.output.add_message(message)

    def run_app(self):

        #Window thread that will clear list and show any active alarms
        self.after(2000, self.after_refresh_active_alarms)

        self.after(2000, self.after_rotate_image)

        self.after(2000, self.thread_manager.start)

        fp = fm.get_reg(r"SOFTWARE\\Plc Data Collector\\")

        try:
            if fp:
                self.main_menu.create_open_file_thread(fp,True)
        except Exception:
            print("Error, Didn't load file, cannot find last file loaded")

        self.left_body_frame.populate_indicators()

        self.mainloop()

