import os
import sys
import traceback
import winreg
import ttkbootstrap as ttk
import openpyxl
from openpyxl import Workbook, load_workbook
from enum import Enum, auto


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def change_theme(theme):
    if theme == 'dark':
        ttk.Style(theme='darkly')

    elif theme == 'light':
        ttk.Style(theme='flatly')
# Function to save data to Excel
def save_to_excel(plc, row):

    #If folder doesn't exist, then create it
    if not os.path.exists(plc.excel_file_location):
        os.makedirs(plc.excel_file_location)

    if row:
        try:
            #If file already exists then open it
            if os.path.exists(plc.file_path):
                wb = load_workbook(plc.file_path)
                ws = wb.active
            #If Excel file doesn't exist then create it
            else:
                #Create excel workbook, take active sheet and name it PLC Data
                #Create initial column headers named: "Timestamp" and then the following tag names
                wb = Workbook()
                ws = wb.active
                ws.title = "PLC Data"
                ws.append(["Timestamp"] + plc.tags)  # Header row

            #Add plc tag data as the next row in the sheet
            ws.append(row)
            #Save and close excel file after logging the tag data
            wb.save(plc.file_path)
            print(f"Data logged: {row} to {plc.file_path}")
        except:
            traceback.print_exc()

class TicketPurpose(Enum):

    # ("message":str, Alarm active:bool)
    UPDATE_ALARMS = auto()
    # (state:bool,"plc.name:str")
    TOGGLE_INDICATOR = auto()

    POPULATE_INDICATORS = auto()

    ACTIVE_ALARMS_CLEAR = auto()

class Ticket:
    def __init__(self, ticket_purpose: TicketPurpose, ticket_value):
        self.ticket_purpose = ticket_purpose
        self.ticket_value = ticket_value


