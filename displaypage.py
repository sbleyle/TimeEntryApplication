from tkinter import *
from tkinter import ttk
import sys
import os
import getpass
import backend
import backend_manager
import pyodbc
from datetime import datetime

def insert_detail():
    engagementcode_client1_selection.insert(END, time_entry_page_orig.code1.get())

def engagementcode_search():
    selection_page = os.system('py -3 entrypage.py')
    print(os.environ.get(selection_page.code1()))
    #os.system('py -3 time_entry_page_orig.py')
    #print(os.environ)
    #engagementcode_client1.delete(0, END)
    #for row in os.environ.get('selected_code'):
        #engagementcode_client1.insert(END, row)
    #print(os.environ.get('code1'))

screen = Tk()

#Pay period field
payperiod_label = Label(text = "Pay Period", width = 30)
payperiod_label.grid(column = 0, row = 0, columnspan = 1, sticky = "w", padx = 5)

payperiod_entry = StringVar()
payperiod1 = ttk.Combobox(screen, textvariable = payperiod_entry, state = 'readonly')
payperiod1['values'] = backend.payperiod_dropdown()
payperiod1.grid(column = 0, row = 1, columnspan = 1, sticky = "we", padx = 5)
payperiod1.get()

#Button to review pay period
add_time_entry = Button(screen, text = "Select")
add_time_entry.grid(column = 3, row = 1, columnspan = 2, sticky = "we", padx = 5, pady = 5)

tabControl = ttk.Notebook(screen) 
tabControl.grid(column = 0, row = 2, sticky = "we", padx = 5, pady = 5, columnspan = 12)
tabControl.grid_configure(sticky = "we")
tabControl.grid_columnconfigure(0, weight = 1)
tabControl.grid_rowconfigure(0, weight = 1)
  
week1 = ttk.Frame(tabControl) 
week2 = ttk.Frame(tabControl)
  
tabControl.add(week1, text ='Week 1') 
tabControl.add(week2, text ='Week 2')
#tabControl.pack(expand = 1, fill ="both") 
tabControl.grid(sticky = "ew")

tab1 = LabelFrame(week1, text = "Time Entry Details")

tab1.grid(column = 0, row = 0, sticky = "we", padx = 5, pady = 5)
tab1.grid_configure(sticky = "we")
tab1.grid_columnconfigure(0, weight = 1)
tab1.grid_rowconfigure(0, weight = 1)

wrapper1 = LabelFrame(week1, text = "Time Entry Details")

wrapper1canvas = Canvas(wrapper1)
wrapper1canvas.grid(column = 0, row = 0, sticky = "ew")

yscrollbar = ttk.Scrollbar(wrapper1, orient = "vertical", command = wrapper1canvas.yview)
yscrollbar.grid(column = 1, row = 0, sticky = "ns")

wrapper1canvas.configure(yscrollcommand = yscrollbar.set)

wrapper1canvas.bind("<Configure>", lambda e: wrapper1canvas.configure(scrollregion = wrapper1canvas.bbox("all")))

wrapper1frame = Frame(wrapper1canvas)
wrapper1frame.grid(column = 0, row = 0, sticky = "ew")

wrapper1canvas.create_window((0,0), window = wrapper1frame, anchor = "nw")

wrapper1.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "ew")

xscrollbar = ttk.Scrollbar(wrapper1, orient = "horizontal", command = wrapper1canvas.xview)
xscrollbar.grid(column = 0, row = 1, sticky = "we")

wrapper1canvas.configure(xscrollcommand = xscrollbar.set)

wrapper1frame.grid_columnconfigure(0, weight = 1)
wrapper1frame.grid_rowconfigure(0, weight = 1)

wrapper1.grid_columnconfigure(0, weight = 1)
wrapper1.grid_rowconfigure(0, weight = 1)

wrapper1canvas.grid_columnconfigure(0, weight = 1)
wrapper1canvas.grid_rowconfigure(0, weight = 1)

#########################################################

tab2 = LabelFrame(week2, text = "Time Entry Details")

tab2.grid(column = 0, row = 0, sticky = "we", padx = 5, pady = 5)
tab2.grid_configure(sticky = "we")
tab2.grid_columnconfigure(0, weight = 1)
tab2.grid_rowconfigure(0, weight = 1)

wrapper2 = LabelFrame(week2, text = "Time Entry Details")

wrapper2canvas = Canvas(wrapper2)
wrapper2canvas.grid(column = 0, row = 0, sticky = "ew")

yscrollbar = ttk.Scrollbar(wrapper2, orient = "vertical", command = wrapper2canvas.yview)
yscrollbar.grid(column = 1, row = 0, sticky = "ns")

wrapper2canvas.configure(yscrollcommand = yscrollbar.set)

wrapper2canvas.bind("<Configure>", lambda e: wrapper2canvas.configure(scrollregion = wrapper2canvas.bbox("all")))

wrapper2frame = Frame(wrapper2canvas)
wrapper2frame.grid(column = 0, row = 0, sticky = "ew")

wrapper2canvas.create_window((0,0), window = wrapper2frame, anchor = "nw")

wrapper2.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "ew")

xscrollbar = ttk.Scrollbar(wrapper2, orient = "horizontal", command = wrapper2canvas.xview)
xscrollbar.grid(column = 0, row = 1, sticky = "we")

wrapper2canvas.configure(xscrollcommand = xscrollbar.set)

wrapper2frame.grid_columnconfigure(0, weight = 1)
wrapper2frame.grid_rowconfigure(0, weight = 1)

wrapper2.grid_columnconfigure(0, weight = 1)
wrapper2.grid_rowconfigure(0, weight = 1)

wrapper2canvas.grid_columnconfigure(0, weight = 1)
wrapper2canvas.grid_rowconfigure(0, weight = 1)

search_icon = PhotoImage(file = r"C:\Users\XL647FS\OneDrive - EY\Documents\repo\EYTimeEntryApplication\Dev\search_icon.png")
search_icon_resize = search_icon.subsample(15,15)

notes_icon = PhotoImage(file = r"C:\Users\XL647FS\OneDrive - EY\Documents\repo\EYTimeEntryApplication\Dev\notes_icon.png")
notes_icon_resize = notes_icon.subsample(35,35)

#Client 1 field
engagementcode_client1 = StringVar()
engagementcode_client1_selection = Entry(wrapper1frame, textvariable = engagementcode_client1, width = 12)
engagementcode_client1_selection.grid(column = 0, row = 3, columnspan = 1)

engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize, command = engagementcode_search)
engagementcode_client1_search.grid(column = 1, row = 3, sticky = "we", padx = 5, pady = 5)

#Client 2 field
engagementcode_client2 = StringVar()
engagementcode_client2_selection = Entry(wrapper1frame, textvariable = engagementcode_client2, width = 12)
engagementcode_client2_selection.grid(column = 0, row = 4, columnspan = 1)

engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
engagementcode_client1_search.grid(column = 1, row = 4, sticky = "we", padx = 5, pady = 5)


s = ttk.Style()
s.configure('Treeview', rowheight= 25)

screen.mainloop()