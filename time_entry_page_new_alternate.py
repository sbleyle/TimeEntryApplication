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
hidden = '7/17/2020 - 7/24/2020'

def view_command():
    x = tab1tree.get_children()
    for item in x:
        tab1tree.delete(item)
    for row in backend.view_detail(os_username):
        tab1tree.insert('', 'end', values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        
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
    curItem = tab1tree.item(tab1tree.focus())
    t1.set(curItem['values'][0])

def delete_selectItem():
    rowid = t1.get()
    backend.delete_selectItem(rowid)
    selected_item = tab1tree.selection()[0] ## get selected item
    tab1tree.delete(selected_item)

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

search_icon = PhotoImage(file = r"C:\Users\XL647FS\OneDrive - EY\Documents\repo\EYTimeEntryApplication\Dev\search_icon.png")
search_icon_resize = search_icon.subsample(15,15)

#Pay period field
payperiod_label = Label(text = "Pay Period", width = 30)
payperiod_label.grid(column = 0, row = 1, columnspan = 3, sticky = "w", padx = 5)

payperiod_entry = StringVar()
payperiod1 = ttk.Combobox(screen, textvariable = payperiod_entry, state = 'readonly')
payperiod1['values'] = backend.payperiod_dropdown()
payperiod1.grid(column = 0, row = 2, columnspan = 3, sticky = "we", padx = 5)
payperiod1.get()

#Button to review pay period
add_time_entry = Button(screen, text = "Select", command = toggle_entry)
add_time_entry.grid(column = 3, row = 2, columnspan = 2, sticky = "we", padx = 5, pady = 5)

#Table for time entries
tabControl = ttk.Notebook(screen) 
tabControl.grid(column = 0, row = 3, sticky = "we", padx = 5, pady = 5)
tabControl.grid_configure(sticky = "we")
tabControl.grid_columnconfigure(0, weight = 1)
tabControl.grid_rowconfigure(0, weight = 1)
  
tab1 = ttk.Frame(tabControl) 
week2tab = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tab5 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Week 1') 
tabControl.add(week2tab, text ='Week 2')
#tabControl.pack(expand = 1, fill ="both") 
tabControl.grid(sticky = "we")

currentday = datetime.today().strftime('%m-%d')

########################################
#Week 1
########################################

#Client field
engagement_label = Label(tab1, text = "Client")
engagement_label.grid(column = 0, row = 0, columnspan = 1, sticky = "w", padx = 5)
 
selected_client = StringVar()
client1 = ttk.Combobox(tab1, textvariable = selected_client, state = 'readonly')
client1['values'] = backend.client_dropdown()
client1.grid(column = 0, row = 1, columnspan = 3, sticky = "we", padx = 5)
client1.get()

#Engagement field
engagement_label = Label(tab1, text = "Engagement")
engagement_label.grid(column = 3, row = 0, columnspan = 1, sticky = "w", padx = 5)
 
selected_engagement = StringVar()
engagement1 = ttk.Combobox(tab1, textvariable = selected_engagement, state = 'readonly', postcommand = lambda: engagement1.configure(value = backend.engagement_dropdown(client1.get())))
engagement1['values'] = backend.engagement_dropdown(client1.get())
engagement1.grid(column = 3, row = 1, columnspan = 3, sticky = "we", padx = 5)

#Engagement Code field
engagement_code_label = Label(tab1, text = "Engagement Code")
engagement_code_label.grid(column = 6, row = 0, columnspan = 2, sticky = "w", padx = 5)
 
selected_code = StringVar()
code1 = ttk.Combobox(tab1, textvariable = selected_client, state = 'readonly')
code1['values'] = backend.client_dropdown()
code1.grid(column = 6, row = 1, columnspan = 2, sticky = "we", padx = 5)
code1.get()

#Weekday hours field example
mondayweek1 = StringVar()
week1_label = Entry(tab1, textvariable = mondayweek1, width = 12)
week1_label.grid(column = 1, row = 2, padx = 5, pady = 5)

mondayweek1 = StringVar()
monday_week1_label = Entry(tab1, textvariable = mondayweek1, width = 12)
monday_week1_label.grid(column = 1, row = 3, padx = 5, pady = 5)

mondayweek2 = StringVar()
monday_week2_label = Entry(tab1, textvariable = mondayweek2, width = 12)
monday_week2_label.grid(column = 1, row = 4, padx = 5, pady = 5)

mondayweek2 = StringVar()
monday_week2_label = Entry(tab1, textvariable = mondayweek2, width = 12)
monday_week2_label.grid(column = 1, row = 5, padx = 5, pady = 5)

tuesdayweek1 = StringVar()
tuesday_week1_label = Entry(tab1, textvariable = tuesdayweek1, width = 12)
tuesday_week1_label.grid(column = 2, row = 2, padx = 5, pady = 5)

tuesdayweek1 = StringVar()
tuesday_week1_label = Entry(tab1, textvariable = tuesdayweek1, width = 12)
tuesday_week1_label.grid(column = 2, row = 3, padx = 5, pady = 5)

tuesdayweek2 = StringVar()
tuesday_week2_label = Entry(tab1, textvariable = tuesdayweek2, width = 12)
tuesday_week2_label.grid(column = 2, row = 4, padx = 5, pady = 5)

tuesdayweek2 = StringVar()
tuesday_week2_label = Entry(tab1, textvariable = tuesdayweek2, width = 12)
tuesday_week2_label.grid(column = 2, row = 5, padx = 5, pady = 5)

wednesdayweek1 = StringVar()
wednesday_week1_label = Entry(tab1, textvariable = wednesdayweek1, width = 12)
wednesday_week1_label.grid(column = 3, row = 2, padx = 5, pady = 5)

wednesdayweek1 = StringVar()
wednesday_week1_label = Entry(tab1, textvariable = wednesdayweek1, width = 12)
wednesday_week1_label.grid(column = 3, row = 3, padx = 5, pady = 5)

wednesdayweek2 = StringVar()
wednesday_week2_label = Entry(tab1, textvariable = wednesdayweek2, width = 12)
wednesday_week2_label.grid(column = 3, row = 4, padx = 5, pady = 5)

wednesdayweek2 = StringVar()
wednesday_week2_label = Entry(tab1, textvariable = wednesdayweek2, width = 12)
wednesday_week2_label.grid(column = 3, row = 5, padx = 5, pady = 5)

thursdayweek1 = StringVar()
thursday_week1_label = Entry(tab1, textvariable = thursdayweek1, width = 12)
thursday_week1_label.grid(column = 4, row = 2, padx = 5, pady = 5)

thursdayweek1 = StringVar()
thursday_week1_label = Entry(tab1, textvariable = thursdayweek1, width = 12)
thursday_week1_label.grid(column = 4, row = 3, padx = 5, pady = 5)

thursdayweek2 = StringVar()
thursday_week2_label = Entry(tab1, textvariable = thursdayweek2, width = 12)
thursday_week2_label.grid(column = 4, row = 4, padx = 5, pady = 5)

thursdayweek2 = StringVar()
thursday_week2_label = Entry(tab1, textvariable = thursdayweek2, width = 12)
thursday_week2_label.grid(column = 4, row = 5, padx = 5, pady = 5)

fridayweek1 = StringVar()
friday_week1_label = Entry(tab1, textvariable = fridayweek1, width = 12)
friday_week1_label.grid(column = 5, row = 2, padx = 5, pady = 5)

fridayweek1 = StringVar()
friday_week1_label = Entry(tab1, textvariable = fridayweek1, width = 12)
friday_week1_label.grid(column = 5, row = 3, padx = 5, pady = 5)

fridayweek2 = StringVar()
friday_week2_label = Entry(tab1, textvariable = fridayweek2, width = 12)
friday_week2_label.grid(column = 5, row = 4, padx = 5, pady = 5)

fridayweek2 = StringVar()
friday_week2_label = Entry(tab1, textvariable = fridayweek2, width = 12)
friday_week2_label.grid(column = 5, row = 5, padx = 5, pady = 5)

saturdayweek1 = StringVar()
saturday_week1_label = Entry(tab1, textvariable = saturdayweek1, width = 12)
saturday_week1_label.grid(column = 6, row = 2, padx = 5, pady = 5)

saturdayweek1 = StringVar()
saturday_week1_label = Entry(tab1, textvariable = saturdayweek1, width = 12)
saturday_week1_label.grid(column = 6, row = 3, padx = 5, pady = 5)

saturdayweek2 = StringVar()
saturday_week2_label = Entry(tab1, textvariable = saturdayweek2, width = 12)
saturday_week2_label.grid(column = 6, row = 4, padx = 5, pady = 5)

saturdayweek2 = StringVar()
saturday_week2_label = Entry(tab1, textvariable = saturdayweek2, width = 12)
saturday_week2_label.grid(column = 6, row = 5, padx = 5, pady = 5)

sundayweek1 = StringVar()
sunday_week1_label = Entry(tab1, textvariable = sundayweek1, width = 12)
sunday_week1_label.grid(column = 7, row = 2, padx = 5, pady = 5)

sundayweek1 = StringVar()
sunday_week1_label = Entry(tab1, textvariable = sundayweek1, width = 12)
sunday_week1_label.grid(column = 7, row = 3, padx = 5, pady = 5)

sundayweek2 = StringVar()
sunday_week2_label = Entry(tab1, textvariable = sundayweek2, width = 12)
sunday_week2_label.grid(column = 7, row = 4, padx = 5, pady = 5)

sundayweek2 = StringVar()
sunday_week2_label = Entry(tab1, textvariable = sundayweek2, width = 12)
sunday_week2_label.grid(column = 7, row = 5, padx = 5, pady = 5)

#Comments field
comments_label = LabelFrame(tab1, text = "Comments")

comments_label.grid(column = 0, row = 6, sticky = "we", columnspan = 14, padx = 5, pady = 5)
comments_label.grid_columnconfigure(0, weight = 1)
comments_label.grid_rowconfigure(5, weight = 1)

comments1 = Text(comments_label, height = 3)
comments1.grid(column = 0, row = 0, sticky = "we", columnspan = 9)

########################################
#Week 2
########################################

week1canvas = Canvas(week2tab)
week1canvas.grid(column = 10, row = 0, sticky = "we", padx = 5, pady = 5)

myframe = Frame(week1canvas)
week1canvas.create_window((0,0), window = myframe, anchor = "nw")

yscrollbar = ttk.Scrollbar(week2tab, orient = VERTICAL, command = week1canvas.yview)
yscrollbar.grid(column = 20, row = 0, sticky = "ns", padx = 5, pady = 5)

week1canvas.configure(yscrollcommand = yscrollbar.set)

week1canvas.bind('<Configure>', lambda e: week1canvas.configure(scrollregion = week1canvas.bbox('all')))

myframe = Frame(week1canvas)
week1canvas.create_window((0,0), window = myframe, anchor = "nw")

#Client 1 field
engagementcode_client1 = StringVar()
engagementcode_client1_selection = Entry(myframe, textvariable = engagementcode_client1, width = 12)
engagementcode_client1_selection.grid(column = 0, row = 3, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 3, sticky = "we", padx = 5, pady = 5)

#Client 2 field
engagementcode_client2 = StringVar()
engagementcode_client2_selection = Entry(myframe, textvariable = engagementcode_client2, width = 12)
engagementcode_client2_selection.grid(column = 0, row = 4, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 4, sticky = "we", padx = 5, pady = 5)

#Client 3 field
engagementcode_client3 = StringVar()
engagementcode_client3_selection = Entry(myframe, textvariable = engagementcode_client3, width = 12)
engagementcode_client3_selection.grid(column = 0, row = 5, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 5, sticky = "we", padx = 5, pady = 5)

#Client 4 field
engagementcode_client4 = StringVar()
engagementcode_client4_selection = Entry(myframe, textvariable = engagementcode_client4, width = 12)
engagementcode_client4_selection.grid(column = 0, row = 6, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 6, sticky = "we", padx = 5, pady = 5)

#Client 5 field
engagementcode_client5 = StringVar()
engagementcode_client5_selection = Entry(myframe, textvariable = engagementcode_client5, width = 12)
engagementcode_client5_selection.grid(column = 0, row = 7, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 7, sticky = "we", padx = 5, pady = 5)

#Client 6 field
engagementcode_client6 = StringVar()
engagementcode_client6_selection = Entry(myframe, textvariable = engagementcode_client6, width = 12)
engagementcode_client6_selection.grid(column = 0, row = 8, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 8, sticky = "we", padx = 5, pady = 5)

#Client 7 field
engagementcode_client7 = StringVar()
engagementcode_client7_selection = Entry(myframe, textvariable = engagementcode_client7, width = 12)
engagementcode_client7_selection.grid(column = 0, row = 9, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 9, sticky = "we", padx = 5, pady = 5)

#Client 8 field
engagementcode_client8 = StringVar()
engagementcode_client8_selection = Entry(myframe, textvariable = engagementcode_client8, width = 12)
engagementcode_client8_selection.grid(column = 0, row = 10, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 10, sticky = "we", padx = 5, pady = 5)

#Client 9 field
engagementcode_client9 = StringVar()
engagementcode_client9_selection = Entry(myframe, textvariable = engagementcode_client9, width = 12)
engagementcode_client9_selection.grid(column = 0, row = 11, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 11, sticky = "we", padx = 5, pady = 5)

#Client 10 field
engagementcode_client10 = StringVar()
engagementcode_client10_selection = Entry(myframe, textvariable = engagementcode_client10, width = 12)
engagementcode_client10_selection.grid(column = 0, row = 12, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 12, sticky = "we", padx = 5, pady = 5)

#Client 11 field
engagementcode_client11 = StringVar()
engagementcode_client11_selection = Entry(myframe, textvariable = engagementcode_client11, width = 12)
engagementcode_client11_selection.grid(column = 0, row = 13, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 13, sticky = "we", padx = 5, pady = 5)

#Client 12 field
engagementcode_client12 = StringVar()
engagementcode_client12_selection = Entry(myframe, textvariable = engagementcode_client12, width = 12)
engagementcode_client12_selection.grid(column = 0, row = 14, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 14, sticky = "we", padx = 5, pady = 5)

#Client 13 field
engagementcode_client13 = StringVar()
engagementcode_client13_selection = Entry(myframe, textvariable = engagementcode_client13, width = 12)
engagementcode_client13_selection.grid(column = 0, row = 15, columnspan = 1)

engagementcode_client1_search = Button(myframe, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 15, sticky = "we", padx = 5, pady = 5)

#Weekday hours field example
mondayweek1 = StringVar()
week1_label = Entry(myframe, textvariable = mondayweek1, width = 12)
week1_label.grid(column = 2, row = 2, padx = 5, pady = 5)

mondayweek1 = StringVar()
monday_week1_label = Entry(myframe, textvariable = mondayweek1, width = 12)
monday_week1_label.grid(column = 2, row = 3, padx = 5, pady = 5)

mondayweek2 = StringVar()
monday_week2_label = Entry(myframe, textvariable = mondayweek2, width = 12)
monday_week2_label.grid(column = 2, row = 4, padx = 5, pady = 5)

mondayweek2 = StringVar()
monday_week2_label = Entry(myframe, textvariable = mondayweek2, width = 12)
monday_week2_label.grid(column = 2, row = 5, padx = 5, pady = 5)

tuesdayweek1 = StringVar()
tuesday_week1_label = Entry(myframe, textvariable = tuesdayweek1, width = 12)
tuesday_week1_label.grid(column = 3, row = 2, padx = 5, pady = 5)

tuesdayweek1 = StringVar()
tuesday_week1_label = Entry(myframe, textvariable = tuesdayweek1, width = 12)
tuesday_week1_label.grid(column = 3, row = 3, padx = 5, pady = 5)

tuesdayweek2 = StringVar()
tuesday_week2_label = Entry(myframe, textvariable = tuesdayweek2, width = 12)
tuesday_week2_label.grid(column = 3, row = 4, padx = 5, pady = 5)

tuesdayweek2 = StringVar()
tuesday_week2_label = Entry(myframe, textvariable = tuesdayweek2, width = 12)
tuesday_week2_label.grid(column = 3, row = 5, padx = 5, pady = 5)

wednesdayweek1 = StringVar()
wednesday_week1_label = Entry(myframe, textvariable = wednesdayweek1, width = 12)
wednesday_week1_label.grid(column = 4, row = 2, padx = 5, pady = 5)

wednesdayweek1 = StringVar()
wednesday_week1_label = Entry(myframe, textvariable = wednesdayweek1, width = 12)
wednesday_week1_label.grid(column = 4, row = 3, padx = 5, pady = 5)

wednesdayweek2 = StringVar()
wednesday_week2_label = Entry(myframe, textvariable = wednesdayweek2, width = 12)
wednesday_week2_label.grid(column = 4, row = 4, padx = 5, pady = 5)

wednesdayweek2 = StringVar()
wednesday_week2_label = Entry(myframe, textvariable = wednesdayweek2, width = 12)
wednesday_week2_label.grid(column = 4, row = 5, padx = 5, pady = 5)

thursdayweek1 = StringVar()
thursday_week1_label = Entry(myframe, textvariable = thursdayweek1, width = 12)
thursday_week1_label.grid(column = 5, row = 2, padx = 5, pady = 5)

thursdayweek1 = StringVar()
thursday_week1_label = Entry(myframe, textvariable = thursdayweek1, width = 12)
thursday_week1_label.grid(column = 5, row = 3, padx = 5, pady = 5)

thursdayweek2 = StringVar()
thursday_week2_label = Entry(myframe, textvariable = thursdayweek2, width = 12)
thursday_week2_label.grid(column = 5, row = 4, padx = 5, pady = 5)

thursdayweek2 = StringVar()
thursday_week2_label = Entry(myframe, textvariable = thursdayweek2, width = 12)
thursday_week2_label.grid(column = 5, row = 5, padx = 5, pady = 5)

fridayweek1 = StringVar()
friday_week1_label = Entry(myframe, textvariable = fridayweek1, width = 12)
friday_week1_label.grid(column = 6, row = 2, padx = 5, pady = 5)

fridayweek1 = StringVar()
friday_week1_label = Entry(myframe, textvariable = fridayweek1, width = 12)
friday_week1_label.grid(column = 6, row = 3, padx = 5, pady = 5)

fridayweek2 = StringVar()
friday_week2_label = Entry(myframe, textvariable = fridayweek2, width = 12)
friday_week2_label.grid(column = 6, row = 4, padx = 5, pady = 5)

fridayweek2 = StringVar()
friday_week2_label = Entry(myframe, textvariable = fridayweek2, width = 12)
friday_week2_label.grid(column = 6, row = 5, padx = 5, pady = 5)

saturdayweek1 = StringVar()
saturday_week1_label = Entry(myframe, textvariable = saturdayweek1, width = 12)
saturday_week1_label.grid(column = 7, row = 2, padx = 5, pady = 5)

saturdayweek1 = StringVar()
saturday_week1_label = Entry(myframe, textvariable = saturdayweek1, width = 12)
saturday_week1_label.grid(column = 7, row = 3, padx = 5, pady = 5)

saturdayweek2 = StringVar()
saturday_week2_label = Entry(myframe, textvariable = saturdayweek2, width = 12)
saturday_week2_label.grid(column = 7, row = 4, padx = 5, pady = 5)

saturdayweek2 = StringVar()
saturday_week2_label = Entry(myframe, textvariable = saturdayweek2, width = 12)
saturday_week2_label.grid(column = 7, row = 5, padx = 5, pady = 5)

sundayweek1 = StringVar()
sunday_week1_label = Entry(myframe, textvariable = sundayweek1, width = 12)
sunday_week1_label.grid(column = 8, row = 2, padx = 5, pady = 5)

sundayweek1 = StringVar()
sunday_week1_label = Entry(myframe, textvariable = sundayweek1, width = 12)
sunday_week1_label.grid(column = 8, row = 3, padx = 5, pady = 5)

sundayweek2 = StringVar()
sunday_week2_label = Entry(myframe, textvariable = sundayweek2, width = 12)
sunday_week2_label.grid(column = 8, row = 4, padx = 5, pady = 5)

sundayweek2 = StringVar()
sunday_week2_label = Entry(myframe, textvariable = sundayweek2, width = 12)
sunday_week2_label.grid(column = 8, row = 5, padx = 5, pady = 5)

#week2_entry_tree_ver_sbar.pack(side = "right", fill = "y")
#idk.pack(side = "left")
#idk.create_window((0,0), window = something, anchor = "nw")
#something.bind("<Configure>", )

#week2_entry_tree_hor_sbar = ttk.Scrollbar(tab1, orient = HORIZONTAL, command = idk.xview)
#week2_entry_tree_hor_sbar.grid(column = 0, row = 20, sticky = "we")
#idk.configure(yscrollcommand = week2_entry_tree_ver_sbar.set, xscrollcommand = week2_entry_tree_hor_sbar.set)

##########################################################################################

#Button to add time entries
add_time_entry = Button(screen, text = "Add time entries")
add_time_entry.grid(column = 0, row = 4, columnspan = 2, sticky = "we", padx = 5, pady = 5)

#Button to view time entries
view_time_entry = Button(screen, text = "Refresh time entries display")
view_time_entry.grid(column = 2, row = 4, columnspan = 3, sticky = "we", padx = 5, pady = 5)

##########################################################################################

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

tab1 = LabelFrame(tab1, text = "Time Entry Details")

tab1.grid(column = 0, row = 11, sticky = "we", padx = 5, pady = 5)
tab1.grid_configure(sticky = "we")
tab1.grid_columnconfigure(0, weight = 1)
tab1.grid_rowconfigure(0, weight = 1)

week1tree = ttk.Treeview(tab1, columns = (1, 2, 3, 4, 5, 6, 7, 8, 9), show = "headings", height = "5")
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

week1tree_ver_sbar = ttk.Scrollbar(tab1, orient = VERTICAL, command = week1tree.yview)
week1tree_ver_sbar.grid(column = 9, row = 0, sticky = "ns")
week1tree_hor_sbar = ttk.Scrollbar(tab1, orient = HORIZONTAL, command = week1tree.xview)
week1tree_hor_sbar.grid(column = 0, row = 2, sticky = "we")
week1tree.configure(yscrollcommand = week1tree_ver_sbar.set, xscrollcommand = week1tree_hor_sbar.set)

#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------

tab1 = LabelFrame(tab2, text = "Time Entry Details")

tab1.grid(column = 0, row = 11, sticky = "we", padx = 5, pady = 5)
tab1.grid_configure(sticky = "we")
tab1.grid_columnconfigure(0, weight = 1)
tab1.grid_rowconfigure(0, weight = 1)
    
week2tree = ttk.Treeview(tab1, columns = (1, 2, 3, 4, 5, 6, 7, 8, 9), show = "headings", height = "5")
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

week2tree_ver_sbar = ttk.Scrollbar(tab1, orient = VERTICAL, command = week2tree.yview)
week2tree_ver_sbar.grid(column = 9, row = 0, sticky = "ns")
week2tree_hor_sbar = ttk.Scrollbar(tab1, orient = HORIZONTAL, command = week2tree.xview)
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

s = ttk.Style()
s.configure('Treeview', rowheight= 25)

screen.mainloop()