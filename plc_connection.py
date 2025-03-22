import pylogix
from datetime import datetime
import time

import utils



class PlcConnection:
    def __init__(self, plc):
        self.plc = plc

        self.PLC = pylogix.PLC


    # Read the tags from the PLC and store in excel file
    def collect_data(self):

        data = self.read_plc_tags()

        if data[0]:
            self.send_acknowledgment()
            utils.save_to_excel(data)
            return True
        elif not data[0]:
            return False, data[1]
        else:
            time.sleep(0.5)
            return None
    # Function to read PLC tags
    def read_plc_tags(self):

        with self.PLC as comm:

            comm.IPAddress = self.plc.ip_address

            # Read trigger signal first
            trigger_response = comm.Read(self.plc.trigger_tag)

            #If we cannot read trigger tag, something is wrong
            if trigger_response.Status != "Success":
                return False, f"Error reading trigger signal from: {self.plc.name}, check correct tag name"

            # Only log data when trigger is active
            elif trigger_response.Value == 1:

                return True, self.get_tag_data(comm)

            else:
                return None

    def get_tag_data(self, comm):

        # Timestamp
        data_row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

        for tag in self.plc.tags:

            response = comm.Read(tag)

            if response.Status == "Success":
                data_row.append(response.Value)
            else:
                data_row.append("Error")

        return data_row
    # Method to send acknowledgment to PLC
    def send_acknowledgment(self):
        with self.PLC as comm:
            comm.IPAddress = self.plc.ip_address
            ack_response = comm.Write(self.plc.ack_tag, 1)  # Send acknowledgment signal
            if ack_response.Status == "Success":
                print("Acknowledgment signal sent to PLC.")
            else:
                print("Error sending acknowledgment signal.")
    # Verify connected to PLC
    def check_plc_connection(self):
        with self.PLC as comm:

            comm.IPAddress = self.plc.ip_address
            response = comm.GetPLCTime()

            if response.Status != "Success":
                return False
            else:
                return True
