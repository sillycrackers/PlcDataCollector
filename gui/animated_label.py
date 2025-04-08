import ttkbootstrap as ttk

class AnimatedLabel(ttk.Frame):
    def __init__(self, parent, text):
        super().__init__(master=parent)

        self.parent = parent
        self.text = text

        #Variables
        self.font = "calibri 18 bold"
        self.font_color = "red"
        self.dots_text = ttk.StringVar()
        self.dot_count = 0

        # Widgets
        self.inner_frame = ttk.Frame(self)
        self.inner_frame.pack(expand=True)

        self.loading_label = ttk.Label(self.inner_frame,text=self.text, font=self.font, foreground=self.font_color)
        self.loading_label.pack(side="left", fill="x", padx=(70,0))

        self.dots_label = ttk.Label(self.inner_frame,width=6, text="",textvariable=self.dots_text, font=self.font, foreground=self.font_color)
        self.dots_label.pack(side="left", expand=True, fill="x")

    def adjust_dots(self):

        output_string = ""
        self.dot_count += 1

        for dot in range(self.dot_count):
            output_string += "."

        if self.dot_count > 5:
            self.dot_count = 0

        self.dots_text.set(output_string)