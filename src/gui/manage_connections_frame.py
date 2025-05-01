import threading
import tkinter as tk

from src import entry_validation
from src.gui.data_entry import DataEntry
from src.plc_connection import PlcConnection, Plc, WriteType
from src.utils import *
from src.gui.animated_label import AnimatedLabel
from src.ticketing_system import *
from src.gui.write_type_selection import WriteTypeSelect



class ManageConnectionsFrame(ttk.Frame):

    def __init__(self, parent_window, main_frame):
        super().__init__(master=parent_window)

        self.main_frame = main_frame
        self.parent_window = parent_window
        self.connections = main_frame.plc_data_connections
        self.main_root_window = main_frame.root_window

        self.parent_window.bind("<Button>", self.on_mouse_click)

        #Variables
        self.applied = False
        self.data_did_not_change = True

        # Entry Variables
        self.name_entry_variable = ttk.StringVar()
        self.ip_address_entry_variable = ttk.StringVar()
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
                                          command=lambda _: self.update_entries(self.option))
        self.option_menu.configure(width=40)
        self.option_menu.pack(side="right", expand=True)
        #Delete Button
        self.delete_button = ttk.Button(self.combo_frame, text="Delete", style='custom.TButton', command=self.run_delete_thread)
        self.delete_button.pack(side='left', padx=5)

        self.combo_frame.pack(pady=(20,0))

        # Inner Frame used for data entries
        self.inner_frame = ttk.Frame(self.base_frame)
        self.inner_frame.pack(padx=20, pady=20)


        #===========Data Entries=============#

        #startrow used to locate data entries on grid relative to the first one placed
        self.start_row = 0

        # Name Validation
        self.name_validation_label = ttk.Label(self.inner_frame, text="", foreground="red", justify='right')
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
        self.tag_list_entry = DataEntry(self.parent_window, self.inner_frame, "Tag List:", self.tag_list_entry_variable,
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

        # Write Type Selection
        self.write_type_frame = tk.Frame(self.inner_frame, background="Pink")
        self.write_type_selection = WriteTypeSelect(self.write_type_frame, self.write_type_selected_variable)
        self.write_type_selection.pack(fill="both", expand=True, pady=16)
        self.write_type_frame.grid(row=self.start_row + 14, column=0, columnspan=2, sticky="w")

        # Select default radiobutton
        self.write_type_selected_variable.set(WriteType.APPEND)

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
        self.apply_button = ttk.Button(self.base_frame, style='custom.TButton', text="Apply Changes", command=self.run_apply_thread)
        self.apply_button.pack(side='right', pady=20, padx=(5,20))
        self.apply_button.config(state="disabled")

        # Ok Button
        self.ok_button = ttk.Button(self.base_frame, text="Ok", style='custom.TButton', command=self.ok)
        self.ok_button.pack(side='right', pady=20, padx=5)

        # Cancel Button
        self.cancel_button = ttk.Button(self.base_frame, text="Cancel", style='custom.TButton', command=parent_window.close)
        self.cancel_button.pack(side='right', pady=20, padx=5)

        # ========================================#

        # Add Tracebacks to detect variable changed
        self.name_entry_variable.trace_add("write", self.callback)
        self.ip_address_entry_variable.trace_add("write", self.callback)
        self.trigger_tag_entry_variable.trace_add("write", self.callback)
        self.ack_tag_entry_variable.trace_add("write", self.callback)
        self.tag_list_entry_variable.trace_add("write", self.callback)
        self.excel_file_name_entry_variable.trace_add("write", self.callback)
        self.excel_file_location_entry_variable.trace_add("write", self.callback)
        self.write_type_selected_variable.trace_add("write", self.callback)

        # hide validation labels initially
        self.hide_validation_labels()

        # Populate entries as soon as window opens with first selected option in list
        self.update_entries(self.option)

    def on_mouse_click(self, var):
        print(f"Active threads: {threading.active_count()}")
        print(f"Keys: {self.connections.keys()}")

    def run_delete_thread(self):

        delete_thread = threading.Thread(target=self.delete_connection, daemon=True)
        delete_thread.start()

    def delete_connection(self):
        if self.option.get() != "Add New PLC...":
            self.obtain_data_control()

            self.main_frame.delete_plc_connection(self.option.get())

            self.release_data_control()

            if len(self.connections) > 0:
                for key in self.connections:
                    selection = key
                    print(selection)
                    break
            else:
                selection = "Add New PLC..."

            self.populate_combo_list()
            self.option.set(selection)
            self.option_menu.set_menu(selection, *self.combo_list)

            self.update_entries(self.option)
        else:
            print("Cannot delete this option")

    def hide_validation_labels(self):
        for label in self.validation_labels:
            self.validation_labels[label].config(text="")

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
        if not entry_validation.check_valid_tag(self.trigger_tag_entry_variable.get().strip()):

            self.validation_labels['trigger'].config(
                text="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row")
            flag = False
        else:
            self.validation_labels['trigger'].config(text="")

        # Validate ack tag entry
        if not entry_validation.check_valid_tag(self.ack_tag_entry_variable.get().strip()):
            self.validation_labels['ack'].config(
                text="Invalid Tag Name, can only be numbers, letters and _\nBut first char can't be number and cannot have two or more _ in a row")
            flag = False
        else:
            self.validation_labels['ack'].config(text="")

        # Validate tag list

        input_string_list = self.tag_list_entry_variable.get().split(',')
        output_string_list = []

        for string in input_string_list:
            output_string_list.append(string.strip())

        if not entry_validation.check_valid_tag_list(output_string_list):
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

    def run_apply_thread(self, ok=False):

        apply_thread = threading.Thread(target=self.apply_changes,args=(ok,) ,daemon=True)
        apply_thread.start()

    def obtain_data_control(self):
        self.main_frame.halt_threads = True

        transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_WAIT_CURSOR, value=self.parent_window))
        transmit(self.main_frame,Ticket(purpose=TicketPurpose.SHOW_ANIMATED_LABEL, value=self.loading_label))

        self.main_frame.read_lock.acquire()
        self.main_frame.comm_lock.acquire()

    def release_data_control(self):
        self.main_frame.comm_lock.release()
        self.main_frame.read_lock.release()
        self.applied = True
        self.data_did_not_change = True
        self.main_frame.file_loaded = True
        self.main_frame.halt_threads = False

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

            self.main_frame.data_changed = True

            if ok_button_pressed:
                self.parent_window.close()
            else:
                ...

    def add_new_connection(self):

        new_plc = Plc(
            name=self.name_entry_variable.get(),
            ip_address=self.ip_address_entry_variable.get(),
            trigger_tag=self.trigger_tag_entry_variable.get(),
            ack_tag=self.ack_tag_entry_variable.get(),
            tags=self.tag_list_entry_variable.get().strip().split(','),
            excel_file_name=self.excel_file_name_entry_variable.get(),
            excel_file_location=self.excel_file_location_entry_variable.get(),
            write_type=self.write_type_selected_variable.get()
        )

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

        print(WriteType.OVERWRITE)

        edit_plc = Plc(
            name=self.name_entry_variable.get(),
            ip_address=self.ip_address_entry_variable.get(),
            trigger_tag=self.trigger_tag_entry_variable.get(),
            ack_tag=self.ack_tag_entry_variable.get(),
            # Fixed bug here that was incorrectly converting string to list
            tags=self.tag_list_entry_variable.get().strip().split(','),
            excel_file_name=self.excel_file_name_entry_variable.get(),
            excel_file_location=self.excel_file_location_entry_variable.get(),
            write_type=self.write_type_selected_variable.get()
        )

        edit_plc_connection = PlcConnection(edit_plc, self.main_frame)

        # Stop threads accessing data so we can edit it
        self.obtain_data_control()

        self.replace_plc_connection(edit_plc_connection, self.connections[old_plc_name])

        # Release locks and update flags for controlling threads, so they can start again
        self.release_data_control()

        print("Changes Applied!")

        # Clear list and populate new list with newly added item to dictionary
        self.populate_combo_list()

        self.combo_list.append("Add New PLC...")

        # Set the selected option for the OptionMenu
        self.option.set(self.name_entry_variable.get())

        # Setup the Option Menu again with new list
        self.option_menu.set_menu(self.option.get(), *self.combo_list)

    def ok(self):

        if self.applied or self.data_did_not_change:
            self.parent_window.close()
        else:
            self.run_apply_thread(ok=True)

    def callback(self, var, index, mode):
        self.data_did_not_change = False
        self.apply_button.config(state="normal")
        self.applied = False



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
                self.write_type_selected_variable.set(self.connections[option.get()].plc.write_type)

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
            self.write_type_selected_variable.set(WriteType.APPEND)

        self.apply_button.config(state="disabled")


    def replace_plc_connection(self, new_plc_connection, old_plc_connection):

        self.connections.pop(old_plc_connection.plc.name)
        self.main_frame.add_plc_connection(new_plc_connection)
