from tkinter import *
from tkinter import ttk
import sys
import os
import getpass
import backend
import backend_manager
import pyodbc
from datetime import datetime

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

os_username = getpass.getuser()

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

def insert_command():
    selected_client = client1.get()
    selected_engagement = engagement1.get()
    payperiod_entry = payperiod1.get()
    date_entry = date1.get()
    hours_entry = hours1.get()
    comments_entry = comments1.get(1.0, END)
    backend.insert_detail(selected_client, selected_engagement, payperiod_entry, date_entry, hours_entry, comments_entry, os_username)
    client1.set('')
    engagement1.set('')
    payperiod1.set('')
    date1.set('')
    hours1.set('')
    comments1.delete(1.0, END)

def submit_command():
    payperiod_entry = payperiod1.get()
    backend.submit_timesheet(payperiod_entry, os_username)
    payperiod1.set('')

def manager_approval_nav():
    os.system('py -3 manager_approval_page.py')

screen = Tk()
screen.title("Time Entry Application")
#heading = Label(text = "Add and Review Time Entries and Timesheets", bg = "grey", fg = "white")
#heading.grid(column = 0, row = 0, columnspan = 16, rowspan = 2)

#Client field
engagement_label = Label(text = "Client", width = 40)
engagement_label.grid(column = 3, row = 1, columnspan = 4, sticky = "w", padx = 5)
 
selected_client = StringVar()
client1 = ttk.Combobox(screen, textvariable = selected_client, state = 'readonly')
client1['values'] = backend.client_dropdown()
client1.grid(column = 3, row = 2, columnspan = 4, sticky = "we", padx = 5)
client1.get()

#Engagement field
engagement_label = Label(text = "Engagement", width = 50)
engagement_label.grid(column = 7, row = 1, columnspan = 5, sticky = "w", padx = 5)
 
selected_engagement = StringVar()
engagement1 = ttk.Combobox(screen, textvariable = selected_engagement, state = 'readonly', postcommand = lambda: engagement1.configure(value = backend.engagement_dropdown(client1.get())))
engagement1['values'] = backend.engagement_dropdown(client1.get())
engagement1.grid(column = 7, row = 2, columnspan = 5, sticky = "we", padx = 5)

#Pay period field
payperiod_label = Label(text = "Pay Period", width = 30)
payperiod_label.grid(column = 0, row = 1, columnspan = 3, sticky = "w", padx = 5)

payperiod_entry = StringVar()
payperiod1 = ttk.Combobox(screen, textvariable = payperiod_entry, state = 'readonly')
payperiod1['values'] = backend.payperiod_dropdown()
payperiod1.grid(column = 0, row = 2, columnspan = 3, sticky = "we", padx = 5)
payperiod1.get()

#Hours field
#hour_label = Label(text = "Hours spent on project", width = 30)
#hour_label.grid(column = 5, row = 3, columnspan = 3, sticky = "w", padx = 5)

#hours_entry = StringVar()
#hours1 = ttk.Combobox(screen, textvariable = hours_entry, state = 'readonly')
#hours1['values'] = backend.hours_dropdown()
#hours1.grid(column = 5, row = 4, columnspan = 3, sticky = "we", padx = 5)

#Comments field
comments_label = LabelFrame(screen, text = "Comments")

comments_label.grid(column = 0, row = 5, sticky = "we", columnspan = 9, padx = 5, pady = 5)
comments_label.grid_columnconfigure(0, weight = 1)
comments_label.grid_rowconfigure(5, weight = 1)

comments1 = Text(comments_label, height = 5)
comments1.grid(column = 0, row = 0, sticky = "we", columnspan = 9)

#Multiple day entry
currentday = datetime.today().strftime('%m-%d')

wrapper1 = LabelFrame(screen, text = "Time Entry Details")

wrapper1.grid(column = 0, row = 6, sticky = "we", columnspan = 8, padx = 5, pady = 5)
wrapper1.grid_configure(sticky = "we")
wrapper1.grid_columnconfigure(0, weight = 1)
wrapper1.grid_rowconfigure(0, weight = 1)

#Week 1 field
week1_label = Label(wrapper1, text = "Week 1",)
week1_label.grid(column = 0, row = 1, columnspan = 1)

#Week 2 field
week2_label = Label(wrapper1, text = "Week 2",)
week2_label.grid(column = 0, row = 3, columnspan = 1)

#Weekday hours field example
monday1_label = Label(wrapper1, text = f"Monday - {currentday}")
monday1_label.grid(column = 1, row = 0, padx = 5, pady = 5)

mondayweek1 = StringVar()
monday_week1_label = Entry(wrapper1, textvariable = mondayweek1, width = 8)
monday_week1_label.grid(column = 1, row = 1, padx = 5, pady = 5)

monday1_label = Label(wrapper1, text = f"Monday - {currentday}")
monday1_label.grid(column = 1, row = 2, padx = 5, pady = 5)

mondayweek2 = StringVar()
monday_week2_label = Entry(wrapper1, textvariable = mondayweek2, width = 8)
monday_week2_label.grid(column = 1, row = 3, padx = 5, pady = 5)

tuesday1_label = Label(wrapper1, text = f"Tuesday - {currentday}")
tuesday1_label.grid(column = 2, row = 0, padx = 5, pady = 5)

tuesdayweek1 = StringVar()
tuesday_week1_label = Entry(wrapper1, textvariable = tuesdayweek1, width = 8)
tuesday_week1_label.grid(column = 2, row = 1, padx = 5, pady = 5)

tuesday2_label = Label(wrapper1, text = f"Tuesday - {currentday}")
tuesday2_label.grid(column = 2, row = 2, padx = 5, pady = 5)

tuesdayweek2 = StringVar()
tuesday_week2_label = Entry(wrapper1, textvariable = tuesdayweek2, width = 8)
tuesday_week2_label.grid(column = 2, row = 3, padx = 5, pady = 5)

wednesday1_label = Label(wrapper1, text = f"Wednesday - {currentday}")
wednesday1_label.grid(column = 3, row = 0, padx = 5, pady = 5)

wednesdayweek1 = StringVar()
wednesday_week1_label = Entry(wrapper1, textvariable = wednesdayweek1, width = 8)
wednesday_week1_label.grid(column = 3, row = 1, padx = 5, pady = 5)

wednesday2_label = Label(wrapper1, text = f"Wednesday - {currentday}")
wednesday2_label.grid(column = 3, row = 2, padx = 5, pady = 5)

wednesdayweek2 = StringVar()
wednesday_week2_label = Entry(wrapper1, textvariable = wednesdayweek2, width = 8)
wednesday_week2_label.grid(column = 3, row = 3, padx = 5, pady = 5)

thursday1_label = Label(wrapper1, text = f"Thursday - {currentday}")
thursday1_label.grid(column = 4, row = 0, padx = 5, pady = 5)

thursdayweek1 = StringVar()
thursday_week1_label = Entry(wrapper1, textvariable = thursdayweek1, width = 8)
thursday_week1_label.grid(column = 4, row = 1, padx = 5, pady = 5)

thursday2_label = Label(wrapper1, text = f"Thursday - {currentday}")
thursday2_label.grid(column = 4, row = 2, padx = 5, pady = 5)

thursdayweek2 = StringVar()
thursday_week2_label = Entry(wrapper1, textvariable = thursdayweek2, width = 8)
thursday_week2_label.grid(column = 4, row = 3, padx = 5, pady = 5)

friday1_label = Label(wrapper1, text = f"Friday - {currentday}")
friday1_label.grid(column = 5, row = 0, padx = 5, pady = 5)

fridayweek1 = StringVar()
friday_week1_label = Entry(wrapper1, textvariable = fridayweek1, width = 8)
friday_week1_label.grid(column = 5, row = 1, padx = 5, pady = 5)

friday2_label = Label(wrapper1, text = f"Friday - {currentday}")
friday2_label.grid(column = 5, row = 2, padx = 5, pady = 5)

fridayweek2 = StringVar()
friday_week2_label = Entry(wrapper1, textvariable = fridayweek2, width = 8)
friday_week2_label.grid(column = 5, row = 3, padx = 5, pady = 5)

saturday1_label = Label(wrapper1, text = f"Saturday - {currentday}")
saturday1_label.grid(column = 6, row = 0, padx = 5, pady = 5)

saturdayweek1 = StringVar()
saturday_week1_label = Entry(wrapper1, textvariable = saturdayweek1, width = 8)
saturday_week1_label.grid(column = 6, row = 1, padx = 5, pady = 5)

saturday2_label = Label(wrapper1, text = f"Saturday - {currentday}")
saturday2_label.grid(column = 6, row = 2, padx = 5, pady = 5)

saturdayweek2 = StringVar()
saturday_week2_label = Entry(wrapper1, textvariable = saturdayweek2, width = 8)
saturday_week2_label.grid(column = 6, row = 3, padx = 5, pady = 5)

sunday1_label = Label(wrapper1, text = f"Sunday - {currentday}")
sunday1_label.grid(column = 7, row = 0, padx = 5, pady = 5)

sundayweek1 = StringVar()
sunday_week1_label = Entry(wrapper1, textvariable = sundayweek1, width = 8)
sunday_week1_label.grid(column = 7, row = 1, padx = 5, pady = 5)

sunday2_label = Label(wrapper1, text = f"Sunday - {currentday}")
sunday2_label.grid(column = 7, row = 2, padx = 5, pady = 5)

sundayweek2 = StringVar()
sunday_week2_label = Entry(wrapper1, textvariable = sundayweek2, width = 8)
sunday_week2_label.grid(column = 7, row = 3, padx = 5, pady = 5)

#Button to add time entry
add_time_entry = Button(screen, text = "Add time entry", fg = "green", command = insert_command)
add_time_entry.grid(column = 0, row = 10, columnspan = 2, sticky = "we", padx = 5, pady = 5)

#Button to view time entries
view_time_entry = Button(screen, text = "View detailed time entries", command = view_command)
view_time_entry.grid(column = 0, row = 11, columnspan = 2, sticky = "we", padx = 5, pady = 5)

#Table showing time entries
wrapper1 = LabelFrame(screen, text = "Time Entry Details")

wrapper1.grid(column = 0, row = 12, sticky = "we", columnspan = 15, padx = 5, pady = 5)
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

#Button to delete time entry
delete_time_entry = Button(screen, text = "Delete time entry", fg = "red", command = delete_selectItem)
delete_time_entry.grid(column = 0, row = 17, columnspan = 2, sticky = "we", padx = 5, pady = 5)

screen.mainloop()