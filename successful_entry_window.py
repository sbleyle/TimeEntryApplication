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
screen.geometry("300x100")
screen.title("Time Entry Application")
heading = Label(text = "Success!", bg = "grey", fg = "white", width = "500", height = "2")
heading.pack()

success_label = Label(text = "The following time entry was successfully added.")
success_label.pack()

okay_button = Button(text = "Okay", command = screen.destroy)
okay_button.pack()

screen.mainloop()