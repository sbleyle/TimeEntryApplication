from tkinter import *
from tkinter import ttk
import tkinter.font as font


class DistanceConverter(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Distance Converter")

        frame = MetersToFeet(self)
        frame.grid(row = 0, column = 0, sticky = "NSEW")

        self.bind("<Return>", frame.calculate_feet)
        self.bind("<KP_Enter>", frame.calculate_feet)

class MetersToFeet(Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.feet_value = StringVar()
        self.meters_value = StringVar()

        meters_label = Label(self, text = "Meters:")
        meters_label.grid(column = 1, row = 1, sticky = "W", ipadx = 5)
        meters_input = Entry(self, textvariable = self.meters_value)
        meters_input.grid(column = 2, row = 1, sticky = "EW")
        meters_input.focus()

        feet_label = Label(self, text = "Feet: ")
        feet_label.grid(column = 1, row = 2, sticky = "W", ipadx = 5)
        feet_display = Label(self, textvariable = self.feet_value)
        feet_display.grid(column = 2, row = 2, sticky = "EW")

        calculate_button = Button(self, text = "Calculate", command = self.calculate_feet)
        calculate_button.grid(column = 1, row = 3, columnspan = 2, sticky = "EW")

        for child in self.winfo_children():
            child.grid_configure(padx = 5, pady = 5)

    def calculate_feet(self, *args):
        try:
            value = float(self.meters_value.get())
            self.feet_value.set('%.3f' % (value * 3.28084))
        except ValueError:
            pass   


root = DistanceConverter()

font.nametofont("TkDefaultFont").configure(size = 15)

root.columnconfigure(0, weight = 1)

root.mainloop()