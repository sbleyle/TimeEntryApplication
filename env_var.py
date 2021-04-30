from tkinter import *
from tkinter import ttk
import sys
import os
import getpass
import backend
import backend_manager
import pyodbc
from datetime import datetime

class Navbar(Frame):
class Toolbar(Frame):
class Statusbar(Frame):
class Main(Frame):

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.statusbar = Statusbar(self, )
        self.toolbar = Toolbar(self, )
        self.navbar = Navbar(self, )
        self.main = Main(self, )

        self.statusbar.pack(side = "bottom", fill = "x")
        self.toolbar.pack(side = "top", fill = "x")
        self.navbar.pack(side = "left", fill = "y")
        self.main.pack(side = "right", fill = "both", expand = True)


if __name__ == "__main__":
    root = Tk()
    MainApplication(root).pack(side = "top", fill = "both", expand = True)
    root.mainloop()