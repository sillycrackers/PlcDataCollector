import pylogix as logix
from datetime import datetime
import time
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

        with logix.PLC(timeout=1) as comm:

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
                    if self.main_frame.halt_threads:
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

        with logix.PLC(timeout=1) as comm:
            comm.IPAddress = self.plc.ip_address

            response = comm.GetPLCTime()

            if response.Status != "Success":
                return False
            else:
                return True

class WriteType(StrEnum):
    APPEND = auto()
    OVERWRITE = auto()

# PLC object for setting up PlcConnection object
class Plc:
    def __init__(self, name='',
                 ip_address='',
                 trigger_tag='',
                 ack_tag='',
                 tags=[],
                 excel_file_name='',
                 excel_file_location='',
                 write_type=WriteType.APPEND
                 ):

        self.name = name
        self.ip_address = ip_address
        self.trigger_tag = trigger_tag
        self.ack_tag = ack_tag
        self.tags = tags
        self.excel_file_name = excel_file_name
        self.excel_file_location = excel_file_location
        self.file_path = f"{excel_file_location}\\{excel_file_name}.xlsx"
        self.write_type = write_type
