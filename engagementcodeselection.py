from tkinter import *
from tkinter import ttk
import sys
import os
import getpass
import backend
import backend_manager
import pyodbc

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

def print_code():
    print(selected_code.get())

os_username = getpass.getuser()

screen = Tk()
screen.title("Time Entry Application")
screen.geometry("1000x400")
#heading = Label(text = "Add and Review Time Entries and Timesheets", bg = "grey", fg = "white")
#heading.grid(column = 0, row = 0, columnspan = 16, rowspan = 2)

#Client field
engagement_label = Label(text = "Client", width = 40)
engagement_label.grid(column = 0, row = 1, columnspan = 4, sticky = "w", padx = 5)
 
selected_client = StringVar()
client1 = ttk.Combobox(screen, textvariable = selected_client, state = 'readonly')
client1['values'] = backend.client_dropdown()
client1.grid(column = 0, row = 2, columnspan = 4, sticky = "we", padx = 5)
client1.get()

#Engagement field
engagement_label = Label(text = "Engagement", width = 50)
engagement_label.grid(column = 0, row = 3, columnspan = 5, sticky = "w", padx = 5)
 
selected_engagement = StringVar()
engagement1 = ttk.Combobox(screen, textvariable = selected_engagement, state = 'readonly', postcommand = lambda: engagement1.configure(value = backend.engagement_dropdown(client1.get())))
engagement1['values'] = backend.engagement_dropdown(client1.get())
engagement1.grid(column = 0, row = 4, columnspan = 5, sticky = "we", padx = 5)

#Engagement Code field
engagementcode_label = Label(text = "Engagement Code", width = 40)
engagementcode_label.grid(column = 0, row = 5, columnspan = 4, sticky = "w", padx = 5)
 
selected_code = StringVar()
code1 = Label(screen, textvariable = selected_code, state = 'readonly', postcommand = lambda: code1.configure(value = backend.engagementcode_dropdown(client1.get(), engagement1.get())))
code1['values'] = backend.client_dropdown()
code1.grid(column = 0, row = 6, columnspan = 4, sticky = "we", padx = 5)
code1.get()

select_button = Button(text = "Select", command = print_code)
select_button.grid(column = 0, row = 7, padx = 5, pady = 5)

screen.mainloop()