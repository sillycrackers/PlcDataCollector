import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog
import openpyxl
import re
import csv

from utils import *

class TextEntryWindow(ttk.Toplevel):
    def __init__(self, text_variable, parent_window):
        super().__init__(master=parent_window)
        self.logo_image = tk.PhotoImage(file=resource_path("gui\\imgs\\data_icon.png"))
        self.iconphoto(False, self.logo_image)
        self.title("Tag List")
        self.parent_window = parent_window

        self.text_variable = text_variable

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Separate tags with commas", font="calibri 20")
        self.title_label.pack()

        self.text_input = tk.Text(self.main_frame)
        self.text_input.pack(fill='both',expand=True, pady=10,padx=10)

        self.text_input.insert('1.0',self.text_variable.get())

        self.insert_csv_button = ttk.Button(self.main_frame, text="Insert Excel/Csv File", command=self.open_csv_excel_file)
        self.insert_csv_button.pack(side="left", padx=20, pady=20)

        self.ok_button = ttk.Button(self.main_frame, text="Ok", width=10, command=self.update_variable)
        self.ok_button.pack(side="left", padx=20, pady=20)

        self.transient(self.parent_window)
        self.protocol('WM_DELETE_WINDOW', self.close)
        self.parent_window.attributes('-disabled', 1)

    def update_variable(self):

        self.text_variable.set(self.text_input.get("1.0", 'end-1c').replace("\n",''))

        self.close()

    def close(self):
        self.parent_window.attributes('-disabled', 0)
        self.destroy()

    def open_csv_excel_file(self):
        file_path = filedialog.askopenfilename()

        output = []

        if file_path.endswith('.xlsx'):

            wb = openpyxl.load_workbook(file_path)
            ws = wb.active

            for row in ws.values:
                for value in row:
                    output.append(row[0])

            output_string = ','.join(output)

            self.text_input.replace('1.0', 'end-1c', output_string)

        elif file_path.endswith('.csv'):
            with open(file_path, newline='') as csv_file:
                reader = csv.reader(csv_file, dialect="excel")
                for row in reader:
                    output += row

                output_string = ','.join(output)

            self.text_input.replace('1.0', 'end-1c', output_string)
