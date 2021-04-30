import os
import sys
import getpass
import pyodbc
import backend
from tkinter import *
from tkinter import ttk

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

os_username = getpass.getuser()

screen = Tk()
#screen.geometry("300x100")
screen.title("Time Entry Application")
heading = Label(text = "Success!", bg = "grey", fg = "white", height = "2")
heading.grid(column = 0, row = 0, sticky = "nsew")

success_label = Label(text = "Your timesheet for the selected pay period was successfully submitted.")
success_label.grid(column = 0, row = 1)

okay_button = Button(text = "Okay", command = screen.destroy)
okay_button.grid(column = 0, row = 2, padx = 5, pady = 5)

screen.mainloop()