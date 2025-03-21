import pylogix as logix
from openpyxl import Workbook, load_workbook
import os
from datetime import datetime
import traceback
import time
import json


class PlcConnection:
    def __init__(self, plc):
        self.plc = plc

    # Function to read PLC tags
    def read_plc_tags(self):

        with logix.PLC() as comm:

            comm.IPAddress = self.plc.ip_address

            # Read trigger signal first
            trigger_response = comm.Read(self.plc.trigger_tag)

            if trigger_response.Status != "Success":
                print(f"Error reading trigger signal: {self.plc.trigger_tag}")
                return None

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

                return data_row

            else:
                ...#print("Trigger not active, no data logged.")

            return None

    # Function to save data to Excel
    def save_to_excel(self, data_row):

        #If folder doesn't exist, then create it
        if not os.path.exists(self.plc.excel_file_location):
            os.makedirs(self.plc.excel_file_location)

        if data_row:
            try:
                #If file already exists then open it
                if os.path.exists(self.plc.file_path):
                    wb = load_workbook(self.plc.file_path)
                    ws = wb.active
                #If Excel file doesn't exist then create it
                else:
                    #Create excel workbook, take active sheet and name it PLC Data
                    #Create initial column headers named: "Timestamp" and then the following tag names
                    wb = Workbook()
                    ws = wb.active
                    ws.title = "PLC Data"
                    ws.append(["Timestamp"] + self.plc.tags)  # Header row

                #Add plc tag data as the next row in the sheet
                ws.append(data_row)
                #Save and close excel file after logging the tag data
                wb.save(self.plc.file_path)
                print(f"Data logged: {data_row} to {self.plc.file_path}")
            except:
                traceback.print_exc()

    # Method to send acknowledgment to PLC
    def send_acknowledgment(self):
        with logix.PLC() as comm:
            comm.IPAddress = self.plc.ip_address
            ack_response = comm.Write(self.plc.ack_tag, 1)  # Send acknowledgment signal
            if ack_response.Status == "Success":
                print("Acknowledgment signal sent to PLC.")
            else:
                print("Error sending acknowledgment signal.")

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
        with logix.PLC() as comm:
            comm.IPAddress = self.plc.ip_address

            response = comm.GetPLCTime()

            if response.Status != "Success":
                return False
            else:
                return True
