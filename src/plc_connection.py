import pylogix as logix
import time
from datetime import datetime
from enum import StrEnum, auto

import src.file_management as fm
import src.ticketing_system as ts


class PlcConnection:
    def __init__(self, plc, main_frame):
        self.plc = plc
        self.main_frame = main_frame
        self.last_trigger = False
        self.last_archive_save_date = datetime.now()
        self.data_to_archive = []

    # Function to read PLC tags
    def read_plc_tags(self):

        with logix.PLC(timeout=3) as comm:

            comm.IPAddress = self.plc.ip_address

            # Read trigger signal first
            trigger_response = comm.Read(self.plc.trigger_tag)

            if trigger_response.Status != "Success":
                ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.OUTPUT_MESSAGE,
                                                         value=f"Error reading trigger signal from {self.plc.name}"))
                return False

            # Only log data when trigger is active
            elif trigger_response.Value == 1 and self.last_trigger == 0:
                # Timestamp
                data_row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                for tag in self.plc.tags:
                    response = comm.Read(tag)
                    if response.Status == "Success":
                        data_row.append(response.Value)
                    else:
                        data_row.append("Error")

                    if self.main_frame.thread_manager.halt_threads:
                        print(f"I got here! {self.plc.name} ")
                        return False

                #Used for a Oneshot to only log data once per trigger
                self.last_trigger = trigger_response.Value
                self.data_to_archive.append(data_row)
                self.archive_data()
                return data_row
            self.last_trigger = trigger_response.Value
            return None

    # Function to send acknowledgment to PLC
    def send_acknowledgment(self):
        with logix.PLC() as comm:
            comm.IPAddress = self.plc.ip_address
            ack_response = comm.Write(self.plc.ack_tag, 1)  # Send acknowledgment signal
            if not ack_response.Status == "Success":
                ts.transmit(self.main_frame,ts.Ticket(purpose=ts.TicketPurpose.OUTPUT_MESSAGE, value="Error sending acknowledgment signal."))

    # Read the tags from the PLC and store in excel file
    def collect_data(self):

        data = self.read_plc_tags()
        if data:
            self.send_acknowledgment()
            fm.save_tag_data_to_excel(plc= self.plc, data_row= data,main_frame=self.main_frame, write_type= self.plc.write_type)
        else:
            time.sleep(0.5)

    def archive_data(self):

        #Save current datetime in variable
        cd = datetime.now()

        #Name of the Excel file that will be saved
        file_name = f"{self.plc.name}_data_archive_{cd.year}_{cd.month}_{cd.day}"
        #Folder where file will be saved
        file_location = f"{self.plc.excel_file_location}\\archive"

        if cd.day != self.last_archive_save_date.day:
            if fm.archive(data_list=self.data_to_archive, archive_file_location=file_location,
                          archive_file_name=file_name, headers=self.plc.tags):
                self.last_archive_save_date = cd
                self.data_to_archive.clear()
                ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.OUTPUT_MESSAGE,
                                                       value=f"Archive file saved to: {file_location}\\{file_name}"))

    # Verify connected to PLC
    def check_plc_connection(self):

        with logix.PLC(timeout=3) as comm:
            comm.IPAddress = self.plc.ip_address

            response = comm.GetPLCTime()

            if response.Status != "Success":
                ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.UPDATE_ALARMS, value=(f"Lost Connection to {self.plc.name}", True)))
                ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.TOGGLE_INDICATOR, value=(False, self.plc.name)))
            else:
                ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.UPDATE_ALARMS, value=(f"Lost Connection to {self.plc.name}", False)))
                ts.transmit(self.main_frame, ts.Ticket(purpose=ts.TicketPurpose.TOGGLE_INDICATOR, value=(True, self.plc.name)))


class WriteType(StrEnum):
    APPEND = "append"
    OVERWRITE = "overwrite"


class TriggerType(StrEnum):
    PLC_TRIGGER = "plc_trigger"
    TIME = "time"
    INTERVAL = "interval"

class IntervalUnit(StrEnum):
    MS = "ms"
    SEC = "secs"
    MIN = "mins"


class SpecificTime:
    def __init__(self, hour=0, minute=0):
        self.hour = hour
        self.minute = minute

class Interval:
    def __init__(self, start_hour=0, start_minute : int = 0, unit : IntervalUnit = IntervalUnit.MS, interval : int = 0):
        self.start_hour = start_hour
        self.start_minute = start_minute
        self.unit = unit
        self.interval = interval


# PLC object for setting up PlcConnection object
class Plc:
    def __init__(self, name='',
                 ip_address='',
                 trigger_type= TriggerType.PLC_TRIGGER,
                 trigger_tag='',
                 specific_time : SpecificTime = None,
                 interval : Interval = None,
                 ack_tag='',
                 tags = [],
                 excel_file_name='',
                 excel_file_location='',
                 write_type=WriteType.APPEND
                 ):

        self.name = name
        self.ip_address = ip_address
        self.trigger_type = trigger_type
        self.trigger_tag = trigger_tag
        self.specific_time = specific_time
        self.interval = interval
        self.ack_tag = ack_tag
        self.tags = tags
        self.excel_file_name = excel_file_name
        self.excel_file_location = excel_file_location
        self.file_path = f"{excel_file_location}\\{excel_file_name}.xlsx"
        self.write_type = write_type


