from ttkbootstrap.scrolled import *

from src.gui.new_output_display import NewOutputDisplay



class RightBodyFrame(ttk.Frame):
    def __init__(self,parent_frame, main_frame):
        super().__init__(master=parent_frame)

        self.parent_frame = parent_frame
        self.main_frame = main_frame

        self.top_frame = ttk.Frame(self)

        self.title_label = ttk.Label(master=self.top_frame, text="Output Messages",font="calibri 14",justify="left")
        self.title_label.pack(fill="x", side="left")

        self.clear_button = ttk.Button(self.top_frame, text="CLear Messages", style='custom.TButton', command=self.clear_output)
        self.clear_button.pack(side="right")

        self.top_frame.pack(fill="both")


        self.output = NewOutputDisplay(parent=self)

        self.output.pack(side="bottom", expand=True, fill="both")

    def clear_output(self):
        self.output.clear_messages()



