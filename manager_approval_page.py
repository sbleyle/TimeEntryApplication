from tkinter import *
from tkinter import ttk
import getpass
import textwrap
import pyodbc
import backend_manager

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

os_username = getpass.getuser()

screen = Tk()
#screen.geometry("900x700")
screen.title("Time Entry Application")
#heading = Label(text = "Review and Approve Timesheets", bg = "grey", fg = "white", width = "500", height = "2")
#heading.pack()

def view_hours_by_client_tree():
    for row in backend_manager.hours_by_client_engagement(payperiod1.get(), submitted1.get()):
        wrapper1tree.insert('', 'end', values = (row[0], row[1], row[2]))

def view_hours_by_day_tree():
    for row in backend_manager.hours_by_day(payperiod1.get(), submitted1.get()):
        wrapper2tree.insert('', 'end', values = (row[0], row[1], row[2]))

def view_notes_by_day_tree():
    for row in backend_manager.notes_by_day_client(payperiod1.get(), submitted1.get()):
        wrapper3tree.insert('', 'end', values = (row[0], row[1], row[2], row[3]))

def unsubmitted_timesheets():
    x = wrapper4tree.get_children()
    for item in x:
        wrapper4tree.delete(item)
    for row in backend_manager.unsubmitted_timesheet_list():
        wrapper4tree.insert('', 'end', values = (row[0], row[1]))

def lock_command():
    payperiod_selected = payperiod1.get()
    employee_selected = submitted1.get()
    backend_manager.lock_timesheet(payperiod_selected, employee_selected, os_username)

def approve_command():
    payperiod_selected = payperiod1.get()
    employee_selected = submitted1.get()
    backend_manager.approve_timesheet(payperiod_selected, employee_selected, os_username)
    payperiod1.set('')
    submitted1.set('')

def reject_command():
    payperiod_selected = payperiod1.get()
    employee_selected = submitted1.get()
    backend_manager.reject_timesheet(payperiod_selected, employee_selected, os_username)
    payperiod1.set('')
    submitted1.set('')

#Pay period field
payperiod_label = Label(text = "Pay Period", width = 25)
payperiod_label.grid(column = 0, row = 1, padx = 5)

payperiod_selection = StringVar()
payperiod1 = ttk.Combobox(screen, width = 22, textvariable = payperiod_selection, state = 'readonly')
payperiod1['values'] = backend_manager.payperiod_dropdown()
payperiod1.grid(column = 0, row = 2, columnspan = 2, padx = 5)
payperiod1.get()

#Submitted list field
employee_label = Label(text = "Submitted Timesheets", width = 25)
employee_label.grid(column = 2, row = 1, padx = 5)

submitted_selection = StringVar()
submitted1 = ttk.Combobox(screen, width = 22, textvariable = submitted_selection, state = 'readonly', postcommand = lambda: submitted1.configure(value = backend_manager.submittedtimesheets(payperiod1.get(), os_username)))
submitted1['values'] = backend_manager.submittedtimesheets(payperiod1.get(), os_username)
submitted1.grid(column = 2, row = 2, columnspan = 2, padx = 5)
submitted1.get()

#Button to lock pay period for selected pay period and selected employee
lock_payperiod = Button(screen, text = "Lock pay period", width = 25, command = lock_command)
lock_payperiod.grid(column = 0, row = 3, columnspan = 2, padx = 5, pady = 5)

#Button to review timesheet for selected pay period and selected employee
review_timesheet = Button(screen, text = "Review timesheet", width = 25, command = lambda: [view_hours_by_client_tree(), view_hours_by_day_tree(), view_notes_by_day_tree()])
review_timesheet.grid(column = 2, row = 3, columnspan = 2, padx = 5, pady = 5)

#Button to approve timesheet
approve_time_sheet = Button(screen, text = "Approve timesheet", fg = "green", width = 25, command = approve_command)
approve_time_sheet.grid(column = 4, row = 3, columnspan = 2, padx = 5, pady = 5)

#Button to reject timesheet
approve_time_sheet = Button(screen, text = "Reject timesheet", fg = "red", width = 25, command = reject_command)
approve_time_sheet.grid(column = 6, row = 3, columnspan = 2, padx = 5, pady = 5)

#Button to reallocate hours
approve_time_sheet = Button(screen, text = "Reallocate Hours", width = 25)
approve_time_sheet.grid(column = 8, row = 3, columnspan = 2, padx = 5, pady = 5)

#Button to review unsubmitted timesheets
approve_time_sheet = Button(screen, text = "Review unsubmitted timesheets", width = 25, command = unsubmitted_timesheets)
approve_time_sheet.grid(column = 4, row = 2, columnspan = 2, padx = 5, pady = 5)

wrapper1 = LabelFrame(screen, text = "Hours by Client and Engagement")
wrapper2 = LabelFrame(screen, text = "Hours by Day")
wrapper3 = LabelFrame(screen, text = "Hours by Day, Client, and Notes")
wrapper4 = LabelFrame(screen, text = "Unsubmitted Timesheets")

wrapper1.grid(column = 0, row = 6, sticky = "we", columnspan = 5, padx = 5, pady = 5)
wrapper1.grid_columnconfigure(0, weight = 1)
wrapper1.grid_rowconfigure(6, weight = 1)
wrapper2.grid(column = 5, row = 6, sticky = "we", columnspan = 5, padx = 5, pady = 5)
wrapper2.grid_columnconfigure(5, weight = 1)
wrapper2.grid_rowconfigure(6, weight = 1)
wrapper3.grid(column = 0, row = 7, sticky = "we", columnspan = 7, padx = 5, pady = 5)
wrapper3.grid_columnconfigure(0, weight = 1)
wrapper3.grid_rowconfigure(7, weight = 1)
wrapper4.grid(column = 7, row = 7, sticky = "we", columnspan = 3, padx = 5, pady = 5)
wrapper4.grid_columnconfigure(7, weight = 1)
wrapper4.grid_rowconfigure(7, weight = 1)

wrapper1tree = ttk.Treeview(wrapper1, columns = (1,2,3), show = "headings", height = "5")
#wrapper1tree.pack(fill = "both", expand = "yes")
wrapper1tree.grid(column = 0, row = 0, sticky = "we", columnspan = 5)

wrapper1tree.heading(1, text = "Client")
wrapper1tree.heading(2, text = "Engagement")
wrapper1tree.heading(3, text = "Hours Worked")
wrapper1tree.column(1, stretch = True, minwidth = 150, width = 75)
wrapper1tree.column(2, stretch = True, minwidth = 150, width = 75)
wrapper1tree.column(3, stretch = True, minwidth = 125, width = 50)

wrapper1tree_ver_sbar = ttk.Scrollbar(wrapper1, orient = VERTICAL, command = wrapper1tree.yview)
wrapper1tree_ver_sbar.grid(column = 4, row = 0, sticky = "ns")
wrapper1tree_hor_sbar = ttk.Scrollbar(wrapper1, orient = HORIZONTAL, command = wrapper1tree.xview)
wrapper1tree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
wrapper1tree.configure(yscrollcommand = wrapper1tree_ver_sbar.set, xscrollcommand = wrapper1tree_hor_sbar.set)

wrapper2tree = ttk.Treeview(wrapper2, columns = (1,2,3), show = "headings", height = "5")
wrapper2tree.grid(column = 0, row = 0, sticky = "we", columnspan = 8)

wrapper2tree.heading(1, text = "Date")
wrapper2tree.heading(2, text = "Weekday")
wrapper2tree.heading(3, text = "Hours Worked")
wrapper2tree.column(1, stretch = True, minwidth = 100, width = 50)
wrapper2tree.column(2, stretch = True, minwidth = 100, width = 50)
wrapper2tree.column(3, stretch = True, minwidth = 100, width = 50)

wrapper2tree_ver_sbar = ttk.Scrollbar(wrapper2, orient = VERTICAL, command = wrapper2tree.yview)
wrapper2tree_ver_sbar.grid(column = 8, row = 0, sticky = "ns")
wrapper2tree_hor_sbar = ttk.Scrollbar(wrapper2, orient = HORIZONTAL, command = wrapper2tree.xview)
wrapper2tree_hor_sbar.grid(column = 5, row = 2, sticky = "we")
wrapper2tree.configure(yscrollcommand = wrapper2tree_ver_sbar.set, xscrollcommand = wrapper2tree_hor_sbar.set)

wrapper3tree = ttk.Treeview(wrapper3, columns = (1,2,3,4), show = "headings", height = "5")
wrapper3tree.grid(column = 0, row = 0, sticky = "we", columnspan = 6)

wrapper3tree.heading(1, text = "Date")
wrapper3tree.heading(2, text = "Client")
wrapper3tree.heading(3, text = "Notes")
wrapper3tree.heading(4, text = "Hours Worked")
wrapper3tree.column(1, stretch = True, minwidth = 100, width = 50)
wrapper3tree.column(2, stretch = True, minwidth = 150, width = 75)
wrapper3tree.column(3, stretch = True, minwidth = 150, width = 75)
wrapper3tree.column(4, stretch = True, minwidth = 100, width = 50)

wrapper3tree_ver_sbar = ttk.Scrollbar(wrapper3, orient = VERTICAL, command = wrapper3tree.yview)
wrapper3tree_ver_sbar.grid(column = 6, row = 0, sticky = "ns")
wrapper3tree_hor_sbar = ttk.Scrollbar(wrapper3, orient = HORIZONTAL, command = wrapper3tree.xview)
wrapper3tree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
wrapper3tree.configure(yscrollcommand = wrapper3tree_ver_sbar.set, xscrollcommand = wrapper3tree_hor_sbar.set)

wrapper4tree = ttk.Treeview(wrapper4, columns = (1,2), show = "headings", height = "5")
wrapper4tree.grid(column = 0, row = 0, sticky = "we", columnspan = 8)

wrapper4tree.heading(1, text = "Name")
wrapper4tree.heading(2, text = "Pay Period")
wrapper4tree.column(1, stretch = True, minwidth = 100, width = 50)
wrapper4tree.column(2, stretch = True, minwidth = 150, width = 75)

wrapper4tree_ver_sbar = ttk.Scrollbar(wrapper4, orient = VERTICAL, command = wrapper4tree.yview)
wrapper4tree_ver_sbar.grid(column = 8, row = 0, sticky = "ns")
wrapper4tree_hor_sbar = ttk.Scrollbar(wrapper4, orient = HORIZONTAL, command = wrapper4tree.xview)
wrapper4tree_hor_sbar.grid(column = 7, row = 2, sticky = "we")
wrapper4tree.configure(yscrollcommand = wrapper4tree_ver_sbar.set, xscrollcommand = wrapper4tree_hor_sbar.set)

screen.mainloop()