import tkinter as tk
from tkinter import *
from tkinter import ttk
import sys
import os
import getpass
import backend
import backend_manager
import pyodbc
from datetime import datetime


class Win1:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x400")
        self.show_widgets()

    def show_widgets(self):
        self.frame = tk.Frame(self.master)
        self.master.title("Window n.1")
        self.search_icon = PhotoImage(file = r"C:\Users\XL647FS\OneDrive - EY\Documents\repo\EYTimeEntryApplication\Dev\search_icon.png")
        self.search_icon_resize = self.search_icon.subsample(1,1)
        self.create_button(self.search_icon, Win2)
        self.create_button(self.search_icon, Win3)
        self.frame.pack()

    def create_button(self, image, _class):
        "Button that creates a new window"
        tk.Button(
            self.frame, image = image,
            command=lambda: self.new_window(_class)).pack()

    def new_window(self, _class):
        self.win = tk.Toplevel(self.master)
        _class(self.win)

    def close_window(self):
        self.master.destroy()

class Win2(Win1):

    def show_widgets(self):
        "A frame with a button to quit the window"
        self.frame = tk.Frame(self.master, bg="red")
        self.quit_button = tk.Button(
            self.frame, text=f"Quit this window n. 2",
            command=self.close_window)
        self.quit_button.pack()
        self.frame.pack()



class Win3(Win2):

    def show_widgets(self):
        self.frame = tk.Frame(self.master, bg="green")
        self.quit_button = tk.Button(
            self.frame, text=f"Quit this window n. 3",
            command=self.close_window)
        self.label = tk.Label(
            self.frame, text="THIS IS ONLY IN THE THIRD WINDOW")
        self.label.pack()
        self.frame.pack()



root = tk.Tk()
app = Win1(root)
root.mainloop()