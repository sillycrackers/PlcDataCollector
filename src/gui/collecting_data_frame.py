from PIL import Image, ImageTk
from PIL.Image import Resampling
import ttkbootstrap as ttk

from src import utils
import src.file_management as fm

class CollectingDataFrame(ttk.Frame):
    def __init__(self, main_frame):
        super().__init__(master=main_frame)

        self.main_frame = main_frame

        #==============Variables===============#

        self.theta = 0

        #=============Grid setup================#

        #Label
        self.grid_columnconfigure(index=0)
        #Loading Image
        self.grid_columnconfigure(index=1)

        self.grid_rowconfigure(index=0)


        #Make new smaller image
        self.img = Image.open(fm.resource_path("src\\gui\\imgs\\loading.png"))
        self.resized_img = self.img.resize(size=(25,25),resample=Image.Resampling.LANCZOS)
        self.img.close()

        #Convert the re-sized image into a TK Image
        self.loading_image = ImageTk.PhotoImage(self.resized_img)

        #================== Widgets =========================#

        #self.label_font = tk.font.Font(font="Calibri",size=26,weight="normal")
        #Add the Tk Image to a label
        self.loading_image_label = ttk.Label(master=self, image=self.loading_image)
        #Text label on left side of image
        self.label = ttk.Label(master=self, text="Running:", font="Calibri 18")

        #===============Place Widgets on Grid================#
        self.label.grid(row=0, column=0, sticky="ew", padx=(0,5), pady=(0,5))
        self.loading_image_label.grid(row=0, column=1, sticky ="nsew")


    def rotate(self):
        if self.theta >= 360:
            self.theta = 0

        rotated_image = self.resized_img.rotate(self.theta, Resampling.BICUBIC)

        self.loading_image = ImageTk.PhotoImage(rotated_image)

        self.theta += 4

        self.loading_image_label.configure(image=self.loading_image)