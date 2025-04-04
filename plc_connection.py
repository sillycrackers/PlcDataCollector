import pylogix as logix
from openpyxl import Workbook, load_workbook
import os
from datetime import datetime
import traceback
import time

from utils import *


class PlcConnection:
    def __init__(self, plc, main_frame):
        self.plc = plc
        self.main_frame = main_frame


    # Function to read PLC tags
    def read_plc_tags(self):

        with logix.PLC() as comm:

            comm.IPAddress = self.plc.ip_address

            # Read trigger signal first
            trigger_response = comm.Read(self.plc.trigger_tag)

            if trigger_response.Status != "Success":
                error_trigger_active_message_ticket = Ticket(purpose=TicketPurpose.OUTPUT_MESSAGE, value=f"Error reading trigger signal from {self.plc.name}",
                                            main_frame=self.main_frame)
                error_trigger_active_message_ticket.transmit()
                return False

            # Only log data when trigger is active
            elif trigger_response.Value == 1:

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

                return data_row

            else:
                print("Trigger not active")
                #trigger_not_active_message_ticket = Ticket(purpose=TicketPurpose.OUTPUT_MESSAGE, value="Trigger not active, no data logged.",
                                          #main_frame=self.main_frame)
                #trigger_not_active_message_ticket.transmit()


            return None

    # Function to save data to Excel
    def save_to_excel(self, data_row):
        # Ensure the folder exists
        if not os.path.exists(self.plc.excel_file_location):
            os.makedirs(self.plc.excel_file_location)
        else:
            print("Directory Already Exists")

        if data_row:
            try:
                if os.path.exists(self.plc.file_path):
                    wb = load_workbook(self.plc.file_path)
                    ws = wb.active
                else:
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "PLC Data"
                    ws.append(["Timestamp"] + self.plc.tags)  # Header row

                ws.append(data_row)
                wb.save(self.plc.file_path)

                data_collected_message_ticket = Ticket(purpose=TicketPurpose.OUTPUT_MESSAGE, value=f"Data collected from {self.plc.name}: {data_row}",
                                            main_frame=self.main_frame)
                data_collected_message_ticket.transmit()

            except:
                traceback.print_exc()

    # Function to send acknowledgment to PLC
    def send_acknowledgment(self):
        with logix.PLC() as comm:
            comm.IPAddress = self.plc.ip_address
            ack_response = comm.Write(self.plc.ack_tag, 1)  # Send acknowledgment signal
            if not ack_response.Status == "Success":
                error_ack_message_ticket = Ticket(purpose=TicketPurpose.OUTPUT_MESSAGE, value="Error sending acknowledgment signal.",
                                            main_frame=self.main_frame)
                error_ack_message_ticket.transmit()





    # Read the tags from the PLC and store in excel file
    def collect_data(self):

        data = self.read_plc_tags()
        if data:
            self.send_acknowledgment()
            self.save_to_excel(data)
        else:
            time.sleep(0.5)

    # Verify connected to PLC
    def check_plc_connection(self):

        with logix.PLC(timeout=1) as comm:
            comm.IPAddress = self.plc.ip_address

            response = comm.GetPLCTime()

            if response.Status != "Success":
                return False
            else:
                return True


