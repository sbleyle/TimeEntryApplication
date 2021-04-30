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

os_username = getpass.getuser()
hidden = '7/17/2020 - 7/24/2020'

def view_command():
    x = wrapper1tree.get_children()
    for item in x:
        wrapper1tree.delete(item)
    for row in backend.view_detail(os_username):
        wrapper1tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        
def refresh_week1():
    week1x = week1tree.get_children()
    for item in week1x:
        week1tree.delete(item)
    for row in backend.week1_by_client_hours(os_username):
        week1tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

def refresh_week2():
    week2x = week2tree.get_children()
    for item in week2x:
        week2tree.delete(item)
    for row in backend.week2_by_client_hours(os_username):
        week2tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

def refresh_combined():
    combinedx = combinedtree.get_children()
    for item in combinedx:
        combinedtree.delete(item)
    for row in backend.weeks_combined(os_username):
        combinedtree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

def selectItem(event):
    curItem = wrapper1tree.item(wrapper1tree.focus())
    t1.set(curItem['values'][0])

def delete_selectItem():
    rowid = t1.get()
    backend.delete_selectItem(rowid)
    selected_item = wrapper1tree.selection()[0] ## get selected item
    wrapper1tree.delete(selected_item)

def submit_command():
    payperiod_entry = payperiod1.get()
    backend.submit_timesheet(payperiod_entry, os_username)
    payperiod1.set('')

def manager_approval_nav():
    os.system('py -3 manager_approval_page.py')

def toggle_entry():
    global hidden
    if hidden:
        payperiod1.get()
    else:
        payperiod1.grid_remove()
    hidden = not hidden

screen = Tk()
screen.title("Time Entry Application")
#heading = Label(text = "Add and Review Time Entries and Timesheets", bg = "grey", fg = "white")
#heading.grid(column = 0, row = 0, columnspan = 16, rowspan = 2)

#Pay period field
payperiod_label = Label(text = "Pay Period", width = 30)
payperiod_label.grid(column = 0, row = 1, columnspan = 3, sticky = "w", padx = 5)

payperiod_entry = StringVar()
payperiod1 = ttk.Combobox(screen, textvariable = payperiod_entry, state = 'readonly')
payperiod1['values'] = backend.payperiod_dropdown()
payperiod1.grid(column = 0, row = 2, columnspan = 3, sticky = "we", padx = 5)
payperiod1.get()

#Button to review pay period
add_time_entry = Button(screen, text = "Review pay period", command = toggle_entry)
add_time_entry.grid(column = 3, row = 2, columnspan = 2, sticky = "we", padx = 5, pady = 5)

#Table showing hours
tabControl = ttk.Notebook(screen) 
tabControl.grid(column = 0, row = 11, sticky = "we", padx = 5, pady = 5, columnspan = 12)
tabControl.grid_configure(sticky = "we")
tabControl.grid_columnconfigure(0, weight = 1)
tabControl.grid_rowconfigure(0, weight = 1)
  
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Week 1') 
tabControl.add(tab2, text ='Week 2')
tabControl.add(tab3, text ="Combined")
#tabControl.pack(expand = 1, fill ="both") 
tabControl.grid(sticky = "we")

frame1 = LabelFrame(tab1, text = "Time Entry Details")

frame1.grid(column = 0, row = 11, sticky = "we", padx = 5, pady = 5)
frame1.grid_configure(sticky = "we")
frame1.grid_columnconfigure(0, weight = 1)
frame1.grid_rowconfigure(0, weight = 1)

week1tree = ttk.Treeview(frame1, columns = (1, 2, 3, 4, 5, 6, 7, 8, 9), show = "headings", height = "5")
week1tree.grid(column = 0, row = 0, sticky = "nsew")
week1tree.grid_configure(sticky = "nsew")
week1tree.grid_columnconfigure(0, weight = 1)
week1tree.grid_rowconfigure(0, weight = 1)

week1tree.column(1, stretch = True, minwidth = 250, width = 250)
week1tree.column(2, stretch = True, minwidth = 125, width = 125)
week1tree.column(3, stretch = True, minwidth = 125, width = 125)
week1tree.column(4, stretch = True, minwidth = 125, width = 125)
week1tree.column(5, stretch = True, minwidth = 125, width = 125)
week1tree.column(6, stretch = True, minwidth = 125, width = 125)
week1tree.column(7, stretch = True, minwidth = 125, width = 125)
week1tree.column(8, stretch = True, minwidth = 125, width = 125)
week1tree.column(9, stretch = True, minwidth = 100, width = 100)

week1tree.heading(1, text='Client', anchor='w')
week1tree.heading(2, text="Monday")
week1tree.heading(3, text="Tuesday")
week1tree.heading(4, text="Wednesday")
week1tree.heading(5, text="Thursday")
week1tree.heading(6, text="Friday")
week1tree.heading(7, text="Saturday")
week1tree.heading(8, text="Sunday")
week1tree.heading(9, text="Total")

week1tree_ver_sbar = ttk.Scrollbar(frame1, orient = VERTICAL, command = week1tree.yview)
week1tree_ver_sbar.grid(column = 9, row = 0, sticky = "ns")
week1tree_hor_sbar = ttk.Scrollbar(frame1, orient = HORIZONTAL, command = week1tree.xview)
week1tree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
week1tree.configure(yscrollcommand = week1tree_ver_sbar.set, xscrollcommand = week1tree_hor_sbar.set)

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

frame2 = LabelFrame(tab2, text = "Time Entry Details")

frame2.grid(column = 0, row = 11, sticky = "we", padx = 5, pady = 5)
frame2.grid_configure(sticky = "we")
frame2.grid_columnconfigure(0, weight = 1)
frame2.grid_rowconfigure(0, weight = 1)
    
week2tree = ttk.Treeview(frame2, columns = (1, 2, 3, 4, 5, 6, 7, 8, 9), show = "headings", height = "5")
week2tree.grid(column = 0, row = 0, sticky = "nsew")
week2tree.grid_configure(sticky = "nsew")
week2tree.grid_columnconfigure(0, weight = 1)
week2tree.grid_rowconfigure(0, weight = 1)
t1 = StringVar()

week2tree.column(1, stretch = True, minwidth = 250, width = 250)
week2tree.column(2, stretch = True, minwidth = 125, width = 125)
week2tree.column(3, stretch = True, minwidth = 125, width = 125)
week2tree.column(4, stretch = True, minwidth = 125, width = 125)
week2tree.column(5, stretch = True, minwidth = 125, width = 125)
week2tree.column(6, stretch = True, minwidth = 125, width = 125)
week2tree.column(7, stretch = True, minwidth = 125, width = 125)
week2tree.column(8, stretch = True, minwidth = 125, width = 125)
week2tree.column(9, stretch = True, minwidth = 100, width = 100)

week2tree.heading(1, text='Client', anchor='w')
week2tree.heading(2, text="Monday")
week2tree.heading(3, text="Tuesday")
week2tree.heading(4, text="Wednesday")
week2tree.heading(5, text="Thursday")
week2tree.heading(6, text="Friday")
week2tree.heading(7, text="Saturday")
week2tree.heading(8, text="Sunday")
week2tree.heading(9, text="Total")

week2tree_ver_sbar = ttk.Scrollbar(frame2, orient = VERTICAL, command = week2tree.yview)
week2tree_ver_sbar.grid(column = 9, row = 0, sticky = "ns")
week2tree_hor_sbar = ttk.Scrollbar(frame2, orient = HORIZONTAL, command = week2tree.xview)
week2tree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
week2tree.configure(yscrollcommand = week2tree_ver_sbar.set, xscrollcommand = week2tree_hor_sbar.set)

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

frame3 = LabelFrame(tab3, text = "Time Entry Details")

frame3.grid(column = 0, row = 11, sticky = "we", padx = 5, pady = 5)
frame3.grid_configure(sticky = "we")
frame3.grid_columnconfigure(0, weight = 1)
frame3.grid_rowconfigure(0, weight = 1)
    
combinedtree = ttk.Treeview(frame3, columns = (1, 2, 3, 4, 5, 6, 7, 8, 9), show = "headings", height = "5")
combinedtree.grid(column = 0, row = 0, sticky = "nsew")
combinedtree.grid_configure(sticky = "nsew")
combinedtree.grid_columnconfigure(0, weight = 1)
combinedtree.grid_rowconfigure(0, weight = 1)
t1 = StringVar()

combinedtree.column(1, stretch = True, minwidth = 250, width = 250)
combinedtree.column(2, stretch = True, minwidth = 125, width = 125)
combinedtree.column(3, stretch = True, minwidth = 125, width = 125)
combinedtree.column(4, stretch = True, minwidth = 125, width = 125)
combinedtree.column(5, stretch = True, minwidth = 125, width = 125)
combinedtree.column(6, stretch = True, minwidth = 125, width = 125)
combinedtree.column(7, stretch = True, minwidth = 125, width = 125)
combinedtree.column(8, stretch = True, minwidth = 125, width = 125)
combinedtree.column(9, stretch = True, minwidth = 100, width = 100)

combinedtree.heading(1, text='Week', anchor='w')
combinedtree.heading(2, text="Monday")
combinedtree.heading(3, text="Tuesday")
combinedtree.heading(4, text="Wednesday")
combinedtree.heading(5, text="Thursday")
combinedtree.heading(6, text="Friday")
combinedtree.heading(7, text="Saturday")
combinedtree.heading(8, text="Sunday")
combinedtree.heading(9, text="Total")

combinedtree_ver_sbar = ttk.Scrollbar(frame3, orient = VERTICAL, command = combinedtree.yview)
combinedtree_ver_sbar.grid(column = 9, row = 0, sticky = "ns")
combinedtree_hor_sbar = ttk.Scrollbar(frame3, orient = HORIZONTAL, command = combinedtree.xview)
combinedtree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
combinedtree.configure(yscrollcommand = combinedtree_ver_sbar.set, xscrollcommand = combinedtree_hor_sbar.set)

#Button to view time entries
view_time_entry = Button(screen, text = "View detailed time entries", command = view_command)
view_time_entry.grid(column = 0, row = 21, columnspan = 2, sticky = "we", padx = 5, pady = 5)

#Table showing time entries
wrapper1 = LabelFrame(screen, text = "Time Entry Details")

wrapper1.grid(column = 0, row = 22, sticky = "we", columnspan = 15, padx = 5, pady = 5)
wrapper1.grid_configure(sticky = "we")
wrapper1.grid_columnconfigure(0, weight = 1)
wrapper1.grid_rowconfigure(0, weight = 1)

wrapper1tree = ttk.Treeview(wrapper1, columns = (1, 2, 3, 4, 5, 6, 7, 8), show = "headings", height = "5")
wrapper1tree.grid(column = 0, row = 0, sticky = "nsew", columnspan = 15)
wrapper1tree.grid_configure(sticky = "nsew")
wrapper1tree.grid_columnconfigure(0, weight = 1)
wrapper1tree.grid_rowconfigure(0, weight = 1)
wrapper1tree.bind('<ButtonRelease-1>', selectItem)
t1 = StringVar()

s = ttk.Style()
s.configure('Treeview', rowheight= 25)

wrapper1tree.column(1, stretch = True, minwidth = 75, width = 75)
wrapper1tree.column(2, stretch = True, minwidth = 200, width = 200)
wrapper1tree.column(3, stretch = True, minwidth = 125, width = 125)
wrapper1tree.column(4, stretch = True, minwidth = 200, width = 200)
wrapper1tree.column(5, stretch = True, minwidth = 250, width = 250)
wrapper1tree.column(6, stretch = True, minwidth = 250, width = 250)
wrapper1tree.column(7, stretch = True, minwidth = 125, width = 125)
wrapper1tree.column(8, stretch = True, minwidth = 175, width = 175)

wrapper1tree.heading(1, text='EntryID', anchor='w')
wrapper1tree.heading(2, text="Pay Period")
wrapper1tree.heading(3, text="Work Date")
wrapper1tree.heading(4, text="Client")
wrapper1tree.heading(5, text="Engagement")
wrapper1tree.heading(6, text="Notes")
wrapper1tree.heading(7, text="Hours Worked")
wrapper1tree.heading(8, text="Status")

wrapper1tree_ver_sbar = ttk.Scrollbar(wrapper1, orient = VERTICAL, command = wrapper1tree.yview)
wrapper1tree_ver_sbar.grid(column = 9, row = 0, sticky = "ns")
wrapper1tree_hor_sbar = ttk.Scrollbar(wrapper1, orient = HORIZONTAL, command = wrapper1tree.xview)
wrapper1tree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
wrapper1tree.configure(yscrollcommand = wrapper1tree_ver_sbar.set, xscrollcommand = wrapper1tree_hor_sbar.set)

screen.mainloop()