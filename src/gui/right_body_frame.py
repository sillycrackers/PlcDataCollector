from ttkbootstrap.scrolled import *

from src.gui.new_output_display import NewOutputDisplay



class RightBodyFrame(ttk.Frame):
    def __init__(self,parent_frame, main_frame):
        super().__init__(master=parent_frame)

        self.parent_frame = parent_frame
        self.main_frame = main_frame

        self.title_label = ttk.Label(master=self, text="Output Messages",font="calibri 14",justify="left")
        self.title_label.pack(fill="x")

        self.output = NewOutputDisplay(parent=self)

        self.output.pack(expand=True, fill="both")


