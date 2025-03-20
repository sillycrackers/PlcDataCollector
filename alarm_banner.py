import tkinter as tk
import ttkbootstrap as ttk

class AlarmBanner(ttk.Frame):
    def __init__(self, parent, alarm_message):
        super().__init__(master=parent)

        self.label = ttk.Label(self, text=alarm_message, font=f"calibri 12 bold", foreground="white", background="#ff5340")
        self.label.pack()

        self.pack()

    def set_text(self, text):
        self.label.config(text=text)

    def add_message(self, message):
        ...