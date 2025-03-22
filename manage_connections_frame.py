import tkinter as tk

import ttkbootstrap as ttk

import entry_validation
from plc import Plc
from data_entry import DataEntry
from plc_connection import PlcConnection
from fonts import *
from utils import *



class ManageConnectionsFrame(ttk.Frame):
    def __init__(self, root_window, connections):
        super().__init__(master=root_window)
        self.root_window = root_window
        self.connections = connections

        # Entry Variables
        self.name_entry_variable = ttk.StringVar()
        self.ip_address_entry_variable = ttk.StringVar()
        self.trigger_tag_entry_variable = ttk.StringVar()
        self.ack_tag_entry_variable = ttk.StringVar()
        self.tag_list_entry_variable = ttk.StringVar()
        self.excel_file_name_entry_variable = ttk.StringVar()
        self.excel_file_location_entry_variable = ttk.StringVar()

        # Add Tracebacks to detect variable changed
        self.name_entry_variable.trace_add("write", self.callback)
        self.ip_address_entry_variable.trace_add("write", self.callback)
        self.trigger_tag_entry_variable.trace_add("write", self.callback)
        self.ack_tag_entry_variable.trace_add("write", self.callback)
        self.tag_list_entry_variable.trace_add("write", self.callback)
        self.excel_file_name_entry_variable.trace_add("write", self.callback)
        self.excel_file_location_entry_variable.trace_add("write", self.callback)

        self.title_label = ttk.Label(self, text="Manage PLC Connections", font=f"{FONT} 28 ")
        self.title_label.pack(fill="both", expand=True, padx=50, pady=20)

        self.main_label_frame = ttk.LabelFrame(self, text="PLC Connections")
        self.main_label_frame.pack(side="top", fill="x", pady=10, padx=10)

        self.combo_list = []

        self.populate_combo_list()

        self.combo_list.append("Add New PLC...")

        self.option = tk.StringVar()

        try:
            if len(list(self.connections)) > 0:
                self.option.set(next(iter(self.connections)))
            else:
                self.option.set("Add New PLC...")
        except StopIteration:
            print("Stop Iteration, no items in dictionary")

        # Option Menu
        self.option_menu = ttk.OptionMenu(self.main_label_frame, self.option, self.option.get(), *self.combo_list,
                                          command=lambda _: self.update_entries(self.option))
        self.option_menu.configure(width=40)
        self.option_menu.pack(pady=20, expand=True)

        # Inner Frame used for data entries
        self.inner_frame = ttk.Frame(self.main_label_frame)
        self.inner_frame.pack(padx=20, pady=20)

        # variable used to locate data entries on grid relative to the first one placed
        self.start_row = 0

        # ===========Data Entries=============#

        # Name Validation
        self.name_validation_label = ttk.Label(self.inner_frame, text="", foreground="red")
        self.name_validation_label.grid(row=self.start_row, column=0, columnspan=2, sticky='e')
        # PLC Name
        self.name_entry = DataEntry(self, self.inner_frame, "Plc Name:", self.name_entry_variable, self.start_row + 1)

        # Ip Address Validation
        self.ip_validation_label = ttk.Label(self.inner_frame, text="", foreground="red", justify='right')
        self.ip_validation_label.grid(row=self.start_row + 2, column=0, columnspan=2, sticky='e')

        # PLC IP Address
        self.ip_address_entry = DataEntry(self, self.inner_frame, "IP Address:", self.ip_address_entry_variable,
                                          self.start_row + 3)

        # Trigger Tag Validation
        self.trigger_validation_label = ttk.Label(self.inner_frame, text="", foreground="red", justify='right')
        self.trigger_validation_label.grid(row=self.start_row + 4, column=0, columnspan=2, sticky='e')
        # Trigger Tag
        self.trigger_tag_entry = DataEntry(self, self.inner_frame, "Trigger Tag:", self.trigger_tag_entry_variable,
                                           self.start_row + 5)

        # Acknowledge Tag Validation
        self.ack_validation_label = ttk.Label(self.inner_frame, text="", foreground="red", justify='right')
        self.ack_validation_label.grid(row=self.start_row + 6, column=0, columnspan=2, sticky='e')
        # Acknowledge Tag
        self.ack_tag_entry = DataEntry(self, self.inner_frame, "Acknowledge Tag:", self.ack_tag_entry_variable,
                                       self.start_row + 7)

        # Tag List Validation
        self.tag_list_validation_label = ttk.Label(self.inner_frame, text="", foreground="red", justify='right')
        self.tag_list_validation_label.grid(row=self.start_row + 8, column=0, columnspan=2, sticky='e')
        # Tag List
        self.tag_list_entry = DataEntry(self.root_window,self.inner_frame, "Tag List:", self.tag_list_entry_variable,
                                        self.start_row + 9, True, "tag_entry")
        # Excel File Name Validation
        self.excel_file_name_validation_label = ttk.Label(self.inner_frame, text="", foreground="red", justify='right')
        self.excel_file_name_validation_label.grid(row=self.start_row + 10, column=0, columnspan=2, sticky='e')
        # Excel File Name
        self.excel_file_name_entry = DataEntry(self, self.inner_frame, "Excel File Name:",
                                               self.excel_file_name_entry_variable, self.start_row + 11)

        # Excel File Location Validation
        self.excel_file_location_validation_label = ttk.Label(self.inner_frame, text="", foreground="red",
                                                              justify='right')
        self.excel_file_location_validation_label.grid(row=self.start_row + 12, column=0, columnspan=2, sticky='e')
        # Excel File Location
        self.excel_file_location_entry = DataEntry(self, self.inner_frame, "File Save Location:",
                                                   self.excel_file_location_entry_variable, self.start_row + 13, True,
                                                   "file_dir")

        # Populate validation label dictionary used for hiding/showing red validation labels
        self.validation_labels = {
            "name": self.name_validation_label,
            "ip": self.ip_validation_label,
            "trigger": self.trigger_validation_label,
            "ack": self.ack_validation_label,
            "tag_list": self.tag_list_validation_label,
            "excel_file_name": self.excel_file_name_validation_label,
            "excel_file_location": self.excel_file_location_validation_label
        }

        # ================Buttons================#

        # Apply Button
        self.apply_button = ttk.Button(self.main_label_frame, text="Apply Changes", command=self.apply_changes)
        self.apply_button.pack(side='right', pady=20, padx=5)
        self.apply_button.config(state="disabled")

        # Ok Button
        self.ok_button = ttk.Button(self.main_label_frame, text="Ok", command=self.ok)
        self.ok_button.pack(side='right', pady=20, padx=5)

        # Cancel Button
        self.cancel_button = ttk.Button(self.main_label_frame, text="Cancel", command=root_window.close)
        self.cancel_button.pack(side='right', pady=20, padx=5)

        # ========================================#


        # hide validation labels initially
        self.hide_validation_labels()

        # Populate entries as soon as window opens with first selected option in list
        self.update_entries(self.option)

    def hide_validation_labels(self):
        for label in self.validation_labels:
            self.validation_labels[label].config(text="")

    def populate_combo_list(self):

        self.combo_list.clear()

        if len(list(self.connections)) > 0:
            for item in self.connections:
                self.combo_list.append(item)

    def validate_entries(self):
        flag = True

        # Validate mame entry
        if not entry_validation.check_valid_name(self.name_entry_variable.get()):
            self.validation_labels['name'].config(text="Invalid name, char limit is 30, cannot be empty")
            flag = False
        else:
            self.validation_labels['name'].config(text="")

        # Validate IP address entry
        if not entry_validation.check_valid_ip(self.ip_address_entry_variable.get()):
            self.validation_labels['ip'].config(text="Invalid IP Address")
            flag = False
        else:
            self.validation_labels['ip'].config(text="")

        # Validate trigger tag entry
        if not entry_validation.check_valid_tag(self.trigger_tag_entry_variable.get()):
            self.validation_labels['trigger'].config(
                text="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row")
            flag = False
        else:
            self.validation_labels['trigger'].config(text="")

        # Validate ack tag entry
        if not entry_validation.check_valid_tag(self.ack_tag_entry_variable.get()):
            self.validation_labels['ack'].config(
                text="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row")
            flag = False
        else:
            self.validation_labels['ack'].config(text="")

        # Validate tag list
        if not entry_validation.check_valid_tag_list(self.tag_list_entry_variable.get().strip().split(',')):
            self.validation_labels['tag_list'].config(
                text="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row")
            flag = False
        else:
            self.validation_labels['tag_list'].config(text="")

        # Validate excel file name  entry
        if not entry_validation.check_valid_file_name(self.excel_file_name_entry_variable.get()):
            self.validation_labels['excel_file_name'].config(
                text=r"Invalid File Name, cannot contain [\w\-.]+$")
            flag = False
        else:
            self.validation_labels['excel_file_name'].config(text="")

        # Validate excel file location entry
        if not entry_validation.check_valid_file_location(self.excel_file_location_entry_variable.get()):
            self.validation_labels['excel_file_location'].config(
                text=r"Invalid directory, directory doesn't exist")
            flag = False
        else:
            self.validation_labels['excel_file_location'].config(text="")

        if flag == False:
            return False
        else:
            return True

    def apply_changes(self):

        if self.validate_entries():

            # Create completely new plc connection if "Add New PLC..." is selected

            if self.option.get() == "Add New PLC...":
                new_plc = Plc(
                    name=self.name_entry_variable.get(),
                    ip_address=self.ip_address_entry_variable.get(),
                    trigger_tag=self.trigger_tag_entry_variable.get(),
                    ack_tag=self.ack_tag_entry_variable.get(),
                    tags=self.tag_list_entry_variable.get().strip().split(','),
                    excel_file_name=self.excel_file_name_entry_variable.get(),
                    excel_file_location=self.excel_file_location_entry_variable.get()
                )

                self.add_plc_connection(PlcConnection(new_plc))

                self.combo_list.insert(-1, new_plc.name)
                self.option.set(new_plc.name)
                self.option_menu.set_menu(new_plc.name, *self.combo_list)

            else:

                # If we are editing an existing connection
                # Create new plc object to replace the one we are editing
                old_plc_name = self.option.get()

                edit_plc = Plc(
                    name=self.name_entry_variable.get(),
                    ip_address=self.ip_address_entry_variable.get(),
                    trigger_tag=self.trigger_tag_entry_variable.get(),
                    ack_tag=self.ack_tag_entry_variable.get(),
                    # Fixed bug here that was incorrectly converting string to list
                    tags=self.tag_list_entry_variable.get().strip().split(','),
                    excel_file_name=self.excel_file_name_entry_variable.get(),
                    excel_file_location=self.excel_file_location_entry_variable.get()
                )

                edit_plc_connection = PlcConnection(edit_plc)

                self.replace_plc_connection(edit_plc_connection, self.connections[old_plc_name])

                # Clear list and populate new list with newly added item to dictionary
                self.populate_combo_list()

                # Set the selected option for the OptionMenu
                self.option.set(self.name_entry_variable.get())

                # Setup the Option Menu again with new list
                self.option_menu.set_menu(self.option.get(), *self.combo_list)

            self.apply_button.config(state="disabled")
            return True
        else:
            return False

    def ok(self):

        if self.apply_changes():
            self.root_window.close()

    def callback(self, var, index, mode):
        self.apply_button.config(state="enabled")

    def update_entries(self, option):

        if not option.get() == "Add New PLC...":
            try:

                self.name_entry_variable.set(self.connections[option.get()].plc.name)
                self.ip_address_entry_variable.set(self.connections[option.get()].plc.ip_address)
                self.trigger_tag_entry_variable.set(self.connections[option.get()].plc.trigger_tag)
                self.ack_tag_entry_variable.set(self.connections[option.get()].plc.ack_tag)
                # Converts tag list into string, and take out white space
                self.tag_list_entry_variable.set(','.join(self.connections[option.get()].plc.tags).strip())

                self.excel_file_name_entry_variable.set(self.connections[option.get()].plc.excel_file_name)
                self.excel_file_location_entry_variable.set(self.connections[option.get()].plc.excel_file_location)

            except KeyError:
                print("Key Error")
        else:
            self.name_entry_variable.set('')
            self.ip_address_entry_variable.set('')
            self.trigger_tag_entry_variable.set('')
            self.ack_tag_entry_variable.set('')
            self.tag_list_entry_variable.set('')
            self.excel_file_name_entry_variable.set('')
            self.excel_file_location_entry_variable.set('')

        self.apply_button.config(state="disabled")

    def add_plc_connection(self, plc_connection):
        self.connections[plc_connection.plc.name] = plc_connection

    def replace_plc_connection(self, new_plc_connection, old_plc_connection):

        self.connections.pop(old_plc_connection.plc.name)
        self.add_plc_connection(new_plc_connection)
