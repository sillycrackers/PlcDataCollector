import threading
import time
import tkinter as tk
from enum import StrEnum

import ttkbootstrap as ttk

from plc_connection import IntervalUnit, Interval, SpecificTime
from src import entry_validation
from src.gui.data_entry import DataEntry
from src.plc_connection import PlcConnection, Plc, WriteType, TriggerType
from src.gui.animated_label import AnimatedLabel
from src.ticketing_system import Ticket, TicketPurpose, transmit
from src.gui.write_type_selection import WriteTypeSelect
from src.gui.delete_prompt import DeletePrompt
from src.gui.trigger_select_entry import TriggerSelectEntry
from src.gui.specific_time_entry import SpecificTimeEntry
from src.gui.interval_entry import IntervalEntry


class Validations(StrEnum):
    NAME = "name"
    IP = "ip"
    SPECIFIC_TIME = "specific_time"
    INTERVAL_START_TIME = "interval_start_time"
    TRIGGER = "trigger"
    ACK = "ack"
    TAG_LIST = "tag_list"
    EXCEL_FILE_NAME = "excel_file_name"
    EXCEL_FILE_LOCATION = "excel_file_location"

class ManageConnectionsFrame(ttk.Frame):

    def __init__(self, parent_window, main_frame):
        super().__init__(master=parent_window)

        self.main_frame = main_frame
        self.parent_window = parent_window
        self.connections = main_frame.plc_data_connections
        self.thread_manager = main_frame.thread_manager
        self.main_root_window = main_frame.root_window

        self.parent_window.bind("<Button>", self.on_mouse_click)

        #Variables
        self.applied = False
        self.data_did_not_change = True

        self.trigger_type_enum_to_string = {
            TriggerType.PLC_TRIGGER: "PLC Trigger",
            TriggerType.TIME: "Specific Time",
            TriggerType.INTERVAL: "Time Interval"
        }
        self.trigger_type_string_to_enum = {
            "PLC Trigger": TriggerType.PLC_TRIGGER,
            "Specific Time": TriggerType.TIME,
            "Time Interval": TriggerType.INTERVAL
        }
        self.interval_unit_string_to_enum = {
            "ms": IntervalUnit.MS,
            "sec": IntervalUnit.SEC,
            "min": IntervalUnit.MIN
        }
        self.interval_unit_enum_to_string = {
            IntervalUnit.MS: "ms",
            IntervalUnit.SEC: "sec",
            IntervalUnit.MIN: "min"
        }

        # True = yes, False = no
        self.delete_response = False
        # When True, indicates user selected yes or no
        self.response = False

        # Entry Variables
        self.name_entry_variable = ttk.StringVar()
        self.ip_address_entry_variable = ttk.StringVar()
        self.trigger_type_entry_variable = ttk.StringVar()
        self.specific_time_hour_entry_variable = ttk.StringVar()
        self.specific_time_minute_entry_variable = ttk.StringVar()
        self.interval_entry_variable = ttk.StringVar()
        self.interval_start_time_hour_variable = ttk.StringVar()
        self.interval_start_time_minute_variable = ttk.StringVar()
        self.interval_unit_entry_variable = ttk.StringVar()
        self.trigger_tag_entry_variable = ttk.StringVar()
        self.ack_tag_entry_variable = ttk.StringVar()
        self.tag_list_entry_variable = ttk.StringVar()
        self.excel_file_name_entry_variable = ttk.StringVar()
        self.excel_file_location_entry_variable = ttk.StringVar()
        self.write_type_selected_variable = ttk.StringVar()

        #====== Main Frame ======#
        self.title_label = ttk.Label(self, text="Manage PLC Connections", font="calibri 28")
        self.title_label.pack(pady=(30,0))
        self.loading_label_frame = ttk.Frame(self, height=34)
        self.loading_label = AnimatedLabel(self.loading_label_frame, text="Loading")
        self.loading_label_frame.pack(fill="y")
        self.header_label = ttk.Label(self, text="Manage Connections",font="calibri 14", justify="left")
        self.header_label.pack(fill="x")
        self.base_frame = ttk.Frame(self, borderwidth=1, relief=tk.SOLID)
        self.base_frame.pack(pady=(0,20))


        self.combo_list = []
        self.populate_combo_list()
        self.option = tk.StringVar()

        try:
            if len(list(self.connections)) > 0:
                self.option.set(next(iter(self.connections)))
            else:
                self.option.set("Add New PLC...")
        except StopIteration:
            print("Stop Iteration, no items in dictionary")

        #Frame for combo and delete button
        self.combo_frame = ttk.Frame(self.base_frame)
        #Option Menu
        self.option_menu = ttk.OptionMenu(self.combo_frame, self.option, self.option.get(), *self.combo_list,
                                          command=lambda _: self.update_entries(self.option), style="Module_Select.TMenubutton")
        self.option_menu.configure(width=20)
        self.option_menu.pack(side="right")
        #Delete Button
        self.delete_button = ttk.Button(self.combo_frame, text="Delete", style='custom.TButton', command=self.run_delete_thread)
        self.delete_button.pack(side='left')

        self.combo_frame.pack(pady=(20,0), padx=(20, 20), expand=True, fill="both")


        #===========Data Entries=============#

        # Inner Frame used for data entries
        self.data_entries_frame = ttk.Frame(self.base_frame)
        self.data_entries_frame.pack(padx=20, pady=20)

        # Module Name
        self.name_entry = DataEntry(parent_window=self.parent_window,
                                    parent=self.data_entries_frame,
                                    label_text="Plc Name:",
                                    text_variable=self.name_entry_variable,
                                    has_validation=True,
                                    validation_message="Invalid name, char limit is 30, cannot be empty"
                                    )
        self.name_entry.pack(expand=True, fill="both")


        # PLC IP Address
        self.ip_address_entry = DataEntry(parent_window=self.parent_window,
                                          parent=self.data_entries_frame,
                                          label_text= "IP Address:",
                                          text_variable=self.ip_address_entry_variable,
                                          has_validation=True,
                                          validation_message="Invalid IP Address"
                                        )
        self.ip_address_entry.pack(expand=True, fill="both")

        # Trigger Type Selection
        self.trigger_type_entry_variable.set("PLC Trigger")
        self.trigger_type_entry = TriggerSelectEntry(parent=self.data_entries_frame,
                                                     text_variable=self.trigger_type_entry_variable,
                                                     command= self.data_changed)
        self.trigger_type_entry.pack(expand=True, fill="both")

        # Trigger frame, used as container for showing/hiding selected trigger type
        self.triggers_container = ttk.Frame(self.data_entries_frame)
        self.triggers_container.pack(expand=True, fill="both")


        # Specific Time Entry
        self.specific_time_entry = SpecificTimeEntry(parent=self.triggers_container,
                                                     hour_text_variable=self.specific_time_hour_entry_variable,
                                                     minute_text_variable=self.specific_time_minute_entry_variable,
                                                     has_validation=True,
                                                     validation_message="hour 0-23             minute 0-59"
                                                     )


        self.interval_unit_entry_variable.set(IntervalUnit.MS)

        # Interval Entry
        self.interval_entry = IntervalEntry(parent=self.triggers_container, interval_text_variable=self.interval_entry_variable,
                                            interval_start_time_hour=self.interval_start_time_hour_variable,
                                            interval_start_time_minute=self.interval_start_time_minute_variable,
                                            interval_unit_entry_variable=self.interval_unit_entry_variable
                                            )

        #TODO --------Trigger, and acknowledge tag frame, show / hide depending on if PLC trigger type is selected


        # Trigger Tag Entry
        self.trigger_tag_entry = DataEntry(parent_window=self.parent_window,
                                           parent=self.triggers_container,
                                           label_text= "Trigger Tag:",
                                           text_variable=self.trigger_tag_entry_variable,
                                           has_validation=True,
                                           validation_message="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row"
                                           )

        # Acknowledge Tag Entry
        self.ack_tag_entry = DataEntry(parent_window=self.parent_window,
                                       parent=self.triggers_container,
                                       label_text= "Acknowledge Tag:",
                                       text_variable=self.ack_tag_entry_variable,
                                       has_validation=True,
                                       validation_message="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row"
                                       )

        # Tag List Entry
        self.tag_list_entry = DataEntry(parent_window=self.parent_window,
                                        parent=self.data_entries_frame,
                                        label_text= "Tag List:",
                                        text_variable=self.tag_list_entry_variable,
                                        has_popup=True,
                                        popup_type="tag_entry",
                                        has_validation=True,
                                        validation_message="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row"
                                        )
        self.tag_list_entry.pack(expand=True, fill="both")

        # Excel File Name Entry
        self.excel_file_name_entry = DataEntry(parent_window=self.parent_window,
                                               parent=self.data_entries_frame,
                                               label_text= "Excel File Name:",
                                               text_variable=self.excel_file_name_entry_variable,
                                               has_validation=True,
                                               validation_message=r"Invalid File Name, cannot contain [\w\-.]+$"
                                               )
        self.excel_file_name_entry.pack(expand=True, fill="both")

        # Excel File Location
        self.excel_file_location_entry =  DataEntry(parent_window=self.parent_window,
                                                    parent=self.data_entries_frame,
                                                    label_text= "File Save Location:",
                                                    text_variable=self.excel_file_location_entry_variable,
                                                    has_popup=True,
                                                    popup_type="file_dir",
                                                    has_validation=True,
                                                    validation_message=r"Invalid directory, directory doesn't exist"
                                                    )
        self.excel_file_location_entry.pack(expand=True, fill="both")

        # Write Type Selection
        self.write_type_frame = ttk.Frame(self.data_entries_frame)
        self.write_type_selection = WriteTypeSelect(self.write_type_frame, self.write_type_selected_variable)
        self.write_type_selection.pack(fill="both", expand=True, pady=16)
        self.write_type_frame.pack(expand=True, fill="both")


        # Select default radiobutton
        self.write_type_selected_variable.set(WriteType.APPEND)

        # Populate validation label dictionary used for hiding/showing red validation labels
        self.show_validation_label = {
            Validations.NAME: self.name_entry.show_validation_message,
            Validations.IP: self.ip_address_entry.show_validation_message,
            Validations.SPECIFIC_TIME: self.specific_time_entry.show_validation_message,
            Validations.INTERVAL_START_TIME: self.interval_entry.show_validation_message,
            Validations.TRIGGER: self.trigger_tag_entry.show_validation_message,
            Validations.ACK: self.ack_tag_entry.show_validation_message,
            Validations.TAG_LIST: self.tag_list_entry.show_validation_message,
            Validations.EXCEL_FILE_NAME: self.excel_file_name_entry.show_validation_message,
            Validations.EXCEL_FILE_LOCATION: self.excel_file_location_entry.show_validation_message

        }

        self.hide_validation_label = {
            Validations.NAME: self.name_entry.hide_validation_message,
            Validations.IP: self.ip_address_entry.hide_validation_message,
            Validations.SPECIFIC_TIME: self.specific_time_entry.hide_validation_message,
            Validations.INTERVAL_START_TIME: self.interval_entry.hide_validation_message,
            Validations.TRIGGER: self.trigger_tag_entry.hide_validation_message,
            Validations.ACK: self.ack_tag_entry.hide_validation_message,
            Validations.TAG_LIST: self.tag_list_entry.hide_validation_message,
            Validations.EXCEL_FILE_NAME: self.excel_file_name_entry.hide_validation_message,
            Validations.EXCEL_FILE_LOCATION: self.excel_file_location_entry.hide_validation_message
        }

        # ================Buttons================#
        # Apply Button
        self.apply_button = ttk.Button(self.base_frame, style='custom.TButton', text="Apply Changes", command=self.run_apply_thread)
        self.apply_button.pack(side='right', pady=20, padx=(5,20))
        self.apply_button.config(state="disabled")

        # Ok Button
        self.ok_button = ttk.Button(self.base_frame, text="Ok", style='custom.TButton', command=self.ok)
        self.ok_button.pack(side='right', pady=20, padx=5)

        # Cancel Button
        self.cancel_button = ttk.Button(self.base_frame, text="Cancel", style='custom.TButton', command = lambda : parent_window.close(not self.data_did_not_change))
        self.cancel_button.pack(side='right', pady=20, padx=5)

        # ========================================#

        #Add tracebacks if value changes
        self.add_tracebacks()

        # hide validation labels initially
        self.hide_validation_labels()

        # Populate entries as soon as window opens with first selected option in list
        self.update_entries(self.option)

        self.data_did_not_change = True

    def show_trigger_type_frame(self):

        trigger_type = self.trigger_type_string_to_enum[self.trigger_type_entry_variable.get()]

        print("Hellooo")

        if trigger_type == TriggerType.PLC_TRIGGER:
            #Show Trigger Tag and Acknowledge Tag entries only
            self.specific_time_entry.pack_forget()
            self.interval_entry.pack_forget()
            self.trigger_tag_entry.pack(expand=True, fill="both")
            self.ack_tag_entry.pack(expand=True, fill="both")


        elif trigger_type == TriggerType.TIME:
            #Show Specific Time entry only
            self.specific_time_entry.pack(expand=True, fill="both")
            self.interval_entry.pack_forget()
            self.trigger_tag_entry.pack_forget()
            self.ack_tag_entry.pack_forget()

        elif trigger_type == TriggerType.INTERVAL:
            #Show Interval Entry only
            self.interval_entry.pack(expand=True, fill="both")
            self.trigger_tag_entry.pack_forget()
            self.ack_tag_entry.pack_forget()
            self.specific_time_entry.pack_forget()
        else:
            print("Invalid Trigger Type")

    def trigger_type_callback(self, var, index, mode):
        self.show_trigger_type_frame()

    def add_tracebacks(self):
        # Add Tracebacks to detect variable changed
        self.name_entry_variable.trace_add("write", self.callback)
        self.ip_address_entry_variable.trace_add("write", self.callback)
        self.trigger_type_entry_variable.trace_add("write", self.trigger_type_callback)
        self.specific_time_hour_entry_variable.trace_add("write", self.callback)
        self.specific_time_minute_entry_variable.trace_add("write", self.callback)
        self.interval_entry_variable.trace_add("write", self.callback)
        self.interval_start_time_hour_variable.trace_add("write", self.callback)
        self.interval_start_time_minute_variable.trace_add("write", self.callback)
        self.trigger_tag_entry_variable.trace_add("write", self.callback)
        self.ack_tag_entry_variable.trace_add("write", self.callback)
        self.tag_list_entry_variable.trace_add("write", self.callback)
        self.excel_file_name_entry_variable.trace_add("write", self.callback)
        self.excel_file_location_entry_variable.trace_add("write", self.callback)

    def on_mouse_click(self, var):
        pass

    def run_delete_thread(self):

        delete_thread = threading.Thread(target=self.delete_connection, daemon=True)
        delete_thread.start()

    def response_callback(self, yes):
        if yes:
            self.delete_response = True
        else:
            self.delete_response = False

        self.response = True

    def delete_connection(self):

        DeletePrompt(parent=self,parent_window=self.parent_window,plc_name=self.option.get(),response_callback=self.response_callback)

        while not self.response:
            time.sleep(0.1)

        if self.delete_response:

            if self.option.get() != "Add New PLC...":
                self.obtain_data_control()

                self.main_frame.delete_plc_connection(self.option.get())

                self.release_data_control()

                if len(self.connections) > 0:
                    for key in self.connections:
                        selection = key
                        break
                else:
                    selection = "Add New PLC..."

                self.populate_combo_list()
                self.option.set(selection)
                self.option_menu.set_menu(selection, *self.combo_list)

                self.update_entries(self.option)

                self.data_did_not_change = True
            else:
                print("Cannot delete this option")

        self.response = False
        self.delete_response = False

    def hide_validation_labels(self):
        for val in Validations:
            self.hide_validation_label[val]()

    def populate_combo_list(self):

        self.combo_list.clear()

        if len(list(self.connections)) > 0:
            for item in self.connections:
                self.combo_list.append(item)

        self.combo_list.append("Add New PLC...")

    def validate_entries(self):
        flag = True

        # Validate name entry
        if not entry_validation.check_valid_name(self.name_entry_variable.get()):
            self.show_validation_label[Validations.NAME]()
            flag = False
        else:
            self.hide_validation_label[Validations.NAME]()

        # Validate IP address entry
        if not entry_validation.check_valid_ip(self.ip_address_entry_variable.get()):
            self.show_validation_label[Validations.IP]()
            flag = False
        else:
            self.hide_validation_label[Validations.IP]()

        if self.trigger_type_string_to_enum[self.trigger_type_entry_variable.get()] == TriggerType.TIME:
            # Validate Specific Time Entry
            if not entry_validation.check_valid_specific_time(hour=self.specific_time_hour_entry_variable.get(),
                                                              minute=self.specific_time_minute_entry_variable.get()):
                self.show_validation_label[Validations.SPECIFIC_TIME]()
                flag = False
            else:
                self.hide_validation_label[Validations.SPECIFIC_TIME]()

        if self.trigger_type_string_to_enum[self.trigger_type_entry_variable.get()] == TriggerType.INTERVAL:
            # Validate Interval Start Time Entry
            if not entry_validation.check_valid_interval_start_time(hour=self.interval_start_time_hour_variable.get(),
                                                                    minute=self.interval_start_time_minute_variable.get()):
                self.show_validation_label[Validations.INTERVAL_START_TIME]()
                flag = False
            else:
                self.hide_validation_label[Validations.INTERVAL_START_TIME]()

        # Validate trigger tag entry
        if not entry_validation.check_valid_tag(self.trigger_tag_entry_variable.get().strip()):

            self.show_validation_label[Validations.TRIGGER]()
            flag = False
        else:
            self.hide_validation_label[Validations.TRIGGER]()

        # Validate ack tag entry
        if not entry_validation.check_valid_tag(self.ack_tag_entry_variable.get().strip()):
            self.show_validation_label[Validations.ACK]()
            flag = False
        else:
            self.hide_validation_label[Validations.ACK]()

        # Validate tag list

        input_string_list = self.tag_list_entry_variable.get().split(',')
        output_string_list = []

        for string in input_string_list:
            output_string_list.append(string.strip())

        if not entry_validation.check_valid_tag_list(output_string_list):
            self.show_validation_label[Validations.TAG_LIST]()
            flag = False
        else:
            self.hide_validation_label[Validations.TAG_LIST]()
        # Validate excel file name  entry
        if not entry_validation.check_valid_file_name(self.excel_file_name_entry_variable.get()):
            self.show_validation_label[Validations.EXCEL_FILE_NAME]()
            flag = False
        else:
            self.hide_validation_label[Validations.EXCEL_FILE_NAME]()

        # Validate excel file location entry
        if not entry_validation.check_valid_file_location(self.excel_file_location_entry_variable.get()):
            self.show_validation_label[Validations.EXCEL_FILE_LOCATION]()
            flag = False
        else:
            self.hide_validation_label[Validations.EXCEL_FILE_LOCATION]()

        if flag == False:
            return False
        else:
            return True

    def run_apply_thread(self, ok=False):

        apply_thread = threading.Thread(target=self.apply_changes,args=(ok,) ,daemon=True)
        apply_thread.start()

    def obtain_data_control(self):

        self.thread_manager.halt_threads = True

        transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_WAIT_CURSOR, value=self.parent_window))
        transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_ANIMATED_LABEL, value=self.loading_label))

        while self.thread_manager.all_threads_done() != True:
            time.sleep(.1)
            print("waiting")

    def release_data_control(self):

        self.data_did_not_change = True
        self.main_frame.file_loaded = True
        self.thread_manager.halt_threads = False

        transmit(self.main_frame, Ticket(purpose=TicketPurpose.ACTIVE_ALARMS_CLEAR, value=None))
        transmit(self.main_frame, Ticket(purpose=TicketPurpose.POPULATE_INDICATORS, value=None))
        transmit(self.main_frame, Ticket(purpose=TicketPurpose.SHOW_NORMAL_CURSOR, value=self.parent_window))
        transmit(self.main_frame, Ticket(purpose=TicketPurpose.HIDE_ANIMATED_LABEL, value=self.loading_label))

    def apply_changes(self, ok_button_pressed=False):

        if self.validate_entries():

            if self.option.get() == "Add New PLC...":

                # Create completely new plc connection if "Add New PLC..." is selected
                self.add_new_connection()
            else:

                # If we are editing an existing connection
                # Create new plc object to replace the one we are editing
               self.edit_existing_connection()

            self.apply_button.config(state="disabled")

            self.applied = True
            if ok_button_pressed:
                self.parent_window.close(not self.data_did_not_change)

    def add_new_connection(self):

        #TODO

        specific_time = SpecificTime(hour=int(self.specific_time_hour_entry_variable.get()),
                                     minute=int(self.specific_time_minute_entry_variable.get()))

        interval = Interval(start_hour=self.interval_start_time_hour_variable.get(),
                            start_minute=int(self.interval_start_time_minute_variable.get()),
                            unit= self.interval_unit_string_to_enum[self.interval_unit_entry_variable.get()],
                            interval=int(self.interval_entry_variable.get()))
        try:

            new_plc = Plc(
                name=self.name_entry_variable.get(),
                ip_address=self.ip_address_entry_variable.get(),
                trigger_type=self.trigger_type_string_to_enum[self.trigger_type_entry_variable.get()],
                trigger_tag=self.trigger_tag_entry_variable.get(),
                specific_time= specific_time,
                interval=interval,
                ack_tag=self.ack_tag_entry_variable.get(),
                tags=self.tag_list_entry_variable.get().strip().split(','),
                excel_file_name=self.excel_file_name_entry_variable.get(),
                excel_file_location=self.excel_file_location_entry_variable.get(),
                write_type=self.write_type_selected_variable.get()
            )
        except Exception:
            print("Error adding new module")


        # Stop threads accessing data so we can edit it
        self.obtain_data_control()

        # Add new connection to dict
        self.main_frame.add_plc_connection(PlcConnection(new_plc, self.main_frame))

        # Release locks and update flags for controlling threads, so they can start again
        self.release_data_control()

        self.combo_list.insert(-1, new_plc.name)
        self.option.set(new_plc.name)
        self.option_menu.set_menu(new_plc.name, *self.combo_list)

    def edit_existing_connection(self):

        old_plc_name = self.option.get()

        specific_time = SpecificTime(hour=int(self.specific_time_hour_entry_variable.get()),
                                     minute=int(self.specific_time_minute_entry_variable.get()))

        interval = Interval(start_hour=self.interval_start_time_hour_variable.get(),
                            start_minute=int(self.interval_start_time_minute_variable.get()),
                            unit=self.interval_unit_string_to_enum[self.interval_unit_entry_variable.get()],
                            interval=int(self.interval_entry_variable.get()))
        try:

            edit_plc = Plc(
                name=self.name_entry_variable.get(),
                ip_address=self.ip_address_entry_variable.get(),
                trigger_type=self.trigger_type_entry_variable.get(),
                trigger_tag=self.trigger_tag_entry_variable.get(),
                specific_time= specific_time,
                interval=interval,
                ack_tag=self.ack_tag_entry_variable.get(),
                tags=self.tag_list_entry_variable.get().strip().split(','),
                excel_file_name=self.excel_file_name_entry_variable.get(),
                excel_file_location=self.excel_file_location_entry_variable.get(),
                write_type=self.write_type_selected_variable.get()
            )
        except Exception:
            print("Error applying settings")

        edit_plc_connection = PlcConnection(edit_plc, self.main_frame)

        # Stop threads accessing data so we can edit it
        self.obtain_data_control()

        self.replace_plc_connection(edit_plc_connection, self.connections[old_plc_name])

        # Release locks and update flags for controlling threads, so they can start again
        self.release_data_control()

        # Clear list and populate new list with newly added item to dictionary
        self.populate_combo_list()

        #self.combo_list.append("Add New PLC...")

        # Set the selected option for the OptionMenu
        self.option.set(self.name_entry_variable.get())

        # Setup the Option Menu again with new list
        self.option_menu.set_menu(self.option.get(), *self.combo_list)

    def ok(self):

        if self.applied or self.data_did_not_change:
            self.parent_window.close(not self.data_did_not_change)
        else:
            self.run_apply_thread(ok=True)

    def callback(self, var, index, mode):
        self.data_changed()

    def data_changed(self):
        self.data_did_not_change = False
        self.apply_button.config(state="normal")
        self.applied = False

    def update_entries(self, option):

        if not option.get() == "Add New PLC...":

            if len(self.connections) > 0:
                selected_plc = self.connections[option.get()].plc
                try:
                     #specific_time
                     #interval

                    self.name_entry_variable.set(selected_plc.name)
                    self.ip_address_entry_variable.set(selected_plc.ip_address)
                    self.trigger_type_entry_variable.set(self.trigger_type_enum_to_string[selected_plc.trigger_type])
                    self.specific_time_hour_entry_variable.set(selected_plc.specific_time.hour)
                    self.specific_time_minute_entry_variable.set(selected_plc.specific_time.minute)
                    self.interval_entry_variable.set(selected_plc.interval.interval)
                    self.interval_start_time_hour_variable.set(selected_plc.interval.start_hour)
                    self.interval_start_time_minute_variable.set(selected_plc.interval.start_minute)
                    self.interval_unit_entry_variable.set(selected_plc.interval.unit)
                    self.trigger_tag_entry_variable.set(selected_plc.trigger_tag)
                    self.ack_tag_entry_variable.set(selected_plc.ack_tag)
                    # Converts tag list into string, and take out white space
                    self.tag_list_entry_variable.set(','.join(selected_plc.tags).strip())
                    self.excel_file_name_entry_variable.set(selected_plc.excel_file_name)
                    self.excel_file_location_entry_variable.set(selected_plc.excel_file_location)
                    self.write_type_selected_variable.set(selected_plc.write_type)

                except KeyError:
                    print("Key Error")
        else:
            self.name_entry_variable.set('')
            self.ip_address_entry_variable.set('')
            self.trigger_tag_entry_variable.set('PLC Trigger')
            self.specific_time_hour_entry_variable.set('0')
            self.specific_time_minute_entry_variable.set('0')
            self.interval_start_time_hour_variable.set('0')
            self.interval_start_time_minute_variable.set('0')
            self.interval_entry_variable.set('1')
            self.interval_unit_entry_variable.set(IntervalUnit.MS)
            self.trigger_tag_entry_variable.set('')
            self.ack_tag_entry_variable.set('')
            self.tag_list_entry_variable.set('')
            self.excel_file_name_entry_variable.set('')
            self.excel_file_location_entry_variable.set('')
            self.write_type_selected_variable.set(WriteType.APPEND)

        self.apply_button.config(state="disabled")

        self.show_trigger_type_frame()
        self.data_did_not_change = True

    def replace_plc_connection(self, new_plc_connection, old_plc_connection):

        self.connections.pop(old_plc_connection.plc.name)
        self.main_frame.add_plc_connection(new_plc_connection)