import os
import sys
import winreg
import ttkbootstrap as ttk
import openpyxl


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def update_registry():

    icon_path = file=resource_path("data_icon.ico")
    try:
        pdc_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r'.pdc\DefaultIcon')
        winreg.SetValueEx(pdc_key,'',0, winreg.REG_SZ, icon_path)
        if pdc_key:
            winreg.CloseKey(pdc_key)
        return True
    except WindowsError:
        print("Cannot change registry")
        return False


def change_theme(theme):
    if theme == 'dark':
        ttk.Style(theme='darkly')

    elif theme == 'light':
        ttk.Style(theme='flatly')

# Function to save data to Excel
def save_to_excel(self, row):

    #If folder doesn't exist, then create it
    if not os.path.exists(self.plc.excel_file_location):
        os.makedirs(self.plc.excel_file_location)

    if row:
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
            ws.append(row)
            #Save and close excel file after logging the tag data
            wb.save(self.plc.file_path)
            print(f"Data logged: {row} to {self.plc.file_path}")
        except:
            traceback.print_exc()

