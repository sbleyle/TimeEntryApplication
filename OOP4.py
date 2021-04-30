from tkinter import *
from tkinter import ttk
import sys
import os
import getpass
import backend
import backend_manager
import pyodbc
from datetime import datetime

class MainPage:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x500")
        self.frame = Frame(self.master)
        self.show_widgets()

    def engagementcode_search(self, text, _class):
        Button(self.frame, text = text, command = lambda: self.new_window(_class))

    def show_widgets(self):
        self.frame = Frame(self.master)
        self.master.title("Time Entry Application")

        #Pay period field
        self.payperiod_label = Label(self.frame, text = "Pay Period", width = 30)
        self.payperiod_label.grid(column = 0, row = 0, columnspan = 1, sticky = "w", padx = 5)

        self.payperiod_entry = StringVar()
        self.payperiod1 = ttk.Combobox(self.frame, textvariable = self.payperiod_entry, state = 'readonly')
        self.payperiod1['values'] = backend.payperiod_dropdown()
        self.payperiod1.grid(column = 0, row = 1, columnspan = 1, sticky = "we", padx = 5)
        self.payperiod1.get()
        #self.frame.pack()

        #Button to review pay period
        self.add_time_entry = Button(self.frame, text = "Select")
        self.add_time_entry.grid(column = 3, row = 1, columnspan = 2, sticky = "we", padx = 5, pady = 5)

        #Tabs for Week 1 and Week 2
        self.tabControl = ttk.Notebook(self.master) 
        self.tabControl.grid(column = 0, row = 2, sticky = "we", padx = 5, pady = 5, columnspan = 12)
        self.tabControl.grid_configure(sticky = "we")
        self.tabControl.grid_columnconfigure(0, weight = 1)
        self.tabControl.grid_rowconfigure(0, weight = 1)

        self.week1 = ttk.Frame(self.tabControl) 
        self.week2 = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.week1, text ='Week 1') 
        self.tabControl.add(self.week2, text ='Week 2')
        #tabControl.pack(expand = 1, fill ="both") 
        self.tabControl.grid(sticky = "ew")

        self.tab1 = LabelFrame(self.week1, text = "Time Entry Details")

        self.tab1.grid(column = 0, row = 0, sticky = "we", padx = 5, pady = 5)
        self.tab1.grid_configure(sticky = "we")
        self.tab1.grid_columnconfigure(0, weight = 1)
        self.tab1.grid_rowconfigure(0, weight = 1)

        self.wrapper1 = LabelFrame(self.week1, text = "Time Entry Details")

        self.wrapper1canvas = Canvas(self.wrapper1)
        self.wrapper1canvas.grid(column = 0, row = 0, sticky = "ew")

        self.yscrollbar = ttk.Scrollbar(self.wrapper1, orient = "vertical", command = self.wrapper1canvas.yview)
        self.yscrollbar.grid(column = 1, row = 0, sticky = "ns")

        self.wrapper1canvas.configure(yscrollcommand = self.yscrollbar.set)

        self.wrapper1canvas.bind("<Configure>", lambda e: self.wrapper1canvas.configure(scrollregion = self.wrapper1canvas.bbox("all")))

        self.wrapper1frame = Frame(self.wrapper1canvas)
        self.wrapper1frame.grid(column = 0, row = 0, sticky = "ew")

        self.wrapper1canvas.create_window((0,0), window = self.wrapper1frame, anchor = "nw")

        self.wrapper1.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "ew")

        self.xscrollbar = ttk.Scrollbar(self.wrapper1, orient = "horizontal", command = self.wrapper1canvas.xview)
        self.xscrollbar.grid(column = 0, row = 1, sticky = "we")

        self.wrapper1canvas.configure(xscrollcommand = self.xscrollbar.set)

        self.wrapper1frame.grid_columnconfigure(0, weight = 1)
        self.wrapper1frame.grid_rowconfigure(0, weight = 1)

        self.wrapper1.grid_columnconfigure(0, weight = 1)
        self.wrapper1.grid_rowconfigure(0, weight = 1)

        self.wrapper1canvas.grid_columnconfigure(0, weight = 1)
        self.wrapper1canvas.grid_rowconfigure(0, weight = 1)

        #########################################################

        self.tab2 = LabelFrame(self.week2, text = "Time Entry Details")

        self.tab2.grid(column = 0, row = 0, sticky = "we", padx = 5, pady = 5)
        self.tab2.grid_configure(sticky = "we")
        self.tab2.grid_columnconfigure(0, weight = 1)
        self.tab2.grid_rowconfigure(0, weight = 1)

        self.wrapper2 = LabelFrame(self.week2, text = "Time Entry Details")

        self.wrapper2canvas = Canvas(self.wrapper2)
        self.wrapper2canvas.grid(column = 0, row = 0, sticky = "ew")

        self.yscrollbar = ttk.Scrollbar(self.wrapper2, orient = "vertical", command = self.wrapper2canvas.yview)
        self.yscrollbar.grid(column = 1, row = 0, sticky = "ns")

        self.wrapper2canvas.configure(yscrollcommand = self.yscrollbar.set)

        self.wrapper2canvas.bind("<Configure>", lambda e: self.wrapper2canvas.configure(scrollregion = self.wrapper2canvas.bbox("all")))

        self.wrapper2frame = Frame(self.wrapper2canvas)
        self.wrapper2frame.grid(column = 0, row = 0, sticky = "ew")

        self.wrapper2canvas.create_window((0,0), window = self.wrapper2frame, anchor = "nw")

        self.wrapper2.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = "ew")

        self.xscrollbar = ttk.Scrollbar(self.wrapper2, orient = "horizontal", command = self.wrapper2canvas.xview)
        self.xscrollbar.grid(column = 0, row = 1, sticky = "we")

        self.wrapper2canvas.configure(xscrollcommand = self.xscrollbar.set)

        self.wrapper2frame.grid_columnconfigure(0, weight = 1)
        self.wrapper2frame.grid_rowconfigure(0, weight = 1)

        self.wrapper2.grid_columnconfigure(0, weight = 1)
        self.wrapper2.grid_rowconfigure(0, weight = 1)

        self.wrapper2canvas.grid_columnconfigure(0, weight = 1)
        self.wrapper2canvas.grid_rowconfigure(0, weight = 1)

        self.search_icon = PhotoImage(file = r"C:\Users\XL647FS\OneDrive - EY\Documents\repo\EYTimeEntryApplication\Dev\search_icon.png")
        self.search_icon_resize = self.search_icon.subsample(15,15)

        self.notes_icon = PhotoImage(file = r"C:\Users\XL647FS\OneDrive - EY\Documents\repo\EYTimeEntryApplication\Dev\notes_icon.png")
        self.notes_icon_resize = self.notes_icon.subsample(35,35)

        #Client 1 field
        self.engagementcode_client1 = StringVar()
        self.engagementcode_client1_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client1, width = 12)
        self.engagementcode_client1_selection.grid(column = 0, row = 3, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize, command = self.new_window)
        self.engagementcode_client1_search.grid(column = 1, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        self.engagementcode_client2 = StringVar()
        self.engagementcode_client2_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client2, width = 12)
        self.engagementcode_client2_selection.grid(column = 0, row = 4, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        self.engagementcode_client3 = StringVar()
        self.engagementcode_client3_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client3, width = 12)
        self.engagementcode_client3_selection.grid(column = 0, row = 5, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        self.engagementcode_client4 = StringVar()
        self.engagementcode_client4_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client4, width = 12)
        self.engagementcode_client4_selection.grid(column = 0, row = 6, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        self.engagementcode_client5 = StringVar()
        self.engagementcode_client5_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client5, width = 12)
        self.engagementcode_client5_selection.grid(column = 0, row = 7, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        self.engagementcode_client6 = StringVar()
        self.engagementcode_client6_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client6, width = 12)
        self.engagementcode_client6_selection.grid(column = 0, row = 8, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        self.engagementcode_client7 = StringVar()
        self.engagementcode_client7_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client7, width = 12)
        self.engagementcode_client7_selection.grid(column = 0, row = 9, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        self.engagementcode_client8 = StringVar()
        self.engagementcode_client8_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client8, width = 12)
        self.engagementcode_client8_selection.grid(column = 0, row = 10, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        self.engagementcode_client9 = StringVar()
        self.engagementcode_client9_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client9, width = 12)
        self.engagementcode_client9_selection.grid(column = 0, row = 11, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        self.engagementcode_client10 = StringVar()
        self.engagementcode_client10_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client10, width = 12)
        self.engagementcode_client10_selection.grid(column = 0, row = 12, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        self.engagementcode_client11 = StringVar()
        self.engagementcode_client11_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client11, width = 12)
        self.engagementcode_client11_selection.grid(column = 0, row = 13, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        self.engagementcode_client12 = StringVar()
        self.engagementcode_client12_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client12, width = 12)
        self.engagementcode_client12_selection.grid(column = 0, row = 14, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        self.engagementcode_client13 = StringVar()
        self.engagementcode_client13_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client13_selection.grid(column = 0, row = 15, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        self.engagementcode_client14 = StringVar()
        self.engagementcode_client14_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client14_selection.grid(column = 0, row = 16, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        self.engagementcode_client15 = StringVar()
        self.engagementcode_client15_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client15_selection.grid(column = 0, row = 17, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        self.engagementcode_client16 = StringVar()
        self.engagementcode_client16_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client16_selection.grid(column = 0, row = 18, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        self.engagementcode_client17 = StringVar()
        self.engagementcode_client17_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client17_selection.grid(column = 0, row = 19, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        self.engagementcode_client18 = StringVar()
        self.engagementcode_client18_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client18_selection.grid(column = 0, row = 20, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        self.engagementcode_client19 = StringVar()
        self.engagementcode_client19_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client19_selection.grid(column = 0, row = 21, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        self.engagementcode_client20 = StringVar()
        self.engagementcode_client20_selection = Entry(self.wrapper1frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client20_selection.grid(column = 0, row = 22, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper1frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 22, sticky = "we", padx = 5, pady = 5)

        #Weekday hours field example
        self.saturdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.saturdayweek1, width = 12)
        self.week1_label.grid(column = 2, row = 2, padx = 5, pady = 5)

        self.saturdayweek1client1 = StringVar()
        self.saturday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client1, width = 12)
        self.saturday_week1_client1.grid(column = 2, row = 3, padx = 5, pady = 5)

        self.saturdayweek1client2 = StringVar()
        self.saturday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client2, width = 12)
        self.saturday_week1_client2.grid(column = 2, row = 4, padx = 5, pady = 5)

        self.saturdayweek1client3 = StringVar()
        self.saturday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client3, width = 12)
        self.saturday_week1_client3.grid(column = 2, row = 5, padx = 5, pady = 5)

        self.saturdayweek1client4 = StringVar()
        self.saturday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client4, width = 12)
        self.saturday_week1_client4.grid(column = 2, row = 6, padx = 5, pady = 5)

        self.saturdayweek1client5 = StringVar()
        self.saturday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client5, width = 12)
        self.saturday_week1_client5.grid(column = 2, row = 7, padx = 5, pady = 5)

        self.saturdayweek1client6 = StringVar()
        self.saturday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client6, width = 12)
        self.saturday_week1_client6.grid(column = 2, row = 8, padx = 5, pady = 5)

        self.saturdayweek1client7 = StringVar()
        self.saturday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client7, width = 12)
        self.saturday_week1_client7.grid(column = 2, row = 9, padx = 5, pady = 5)

        self.saturdayweek1client8 = StringVar()
        self.saturday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client8, width = 12)
        self.saturday_week1_client8.grid(column = 2, row = 10, padx = 5, pady = 5)

        self.saturdayweek1client9 = StringVar()
        self.saturday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client9, width = 12)
        self.saturday_week1_client9.grid(column = 2, row = 11, padx = 5, pady = 5)

        self.saturdayweek1client10 = StringVar()
        self.saturday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client10, width = 12)
        self.saturday_week1_client10.grid(column = 2, row = 12, padx = 5, pady = 5)

        self.saturdayweek1client11 = StringVar()
        self.saturday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client11, width = 12)
        self.saturday_week1_client11.grid(column = 2, row = 13, padx = 5, pady = 5)

        self.saturdayweek1client12 = StringVar()
        self.saturday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client12, width = 12)
        self.saturday_week1_client12.grid(column = 2, row = 14, padx = 5, pady = 5)

        self.saturdayweek1client13 = StringVar()
        self.saturday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client13, width = 12)
        self.saturday_week1_client13.grid(column = 2, row = 15, padx = 5, pady = 5)

        self.saturdayweek1client14 = StringVar()
        self.saturday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client14, width = 12)
        self.saturday_week1_client14.grid(column = 2, row = 16, padx = 5, pady = 5)

        self.saturdayweek1client15 = StringVar()
        self.saturday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client15, width = 12)
        self.saturday_week1_client15.grid(column = 2, row = 17, padx = 5, pady = 5)

        self.saturdayweek1client16 = StringVar()
        self.saturday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client16, width = 12)
        self.saturday_week1_client16.grid(column = 2, row = 18, padx = 5, pady = 5)

        self.saturdayweek1client17 = StringVar()
        self.saturday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client17, width = 12)
        self.saturday_week1_client17.grid(column = 2, row = 19, padx = 5, pady = 5)

        self.saturdayweek1client18 = StringVar()
        self.saturday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client18, width = 12)
        self.saturday_week1_client18.grid(column = 2, row = 20, padx = 5, pady = 5)

        self.saturdayweek1client19 = StringVar()
        self.saturday_week1_client19= Entry(self.wrapper1frame, textvariable = self.saturdayweek1client19, width = 12)
        self.saturday_week1_client19.grid(column = 2, row = 21, padx = 5, pady = 5)

        self.saturdayweek1client20 = StringVar()
        self.saturday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.saturdayweek1client20, width = 12)
        self.saturday_week1_client20.grid(column = 2, row = 22, padx = 5, pady = 5)

        self.sundayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.sundayweek1, width = 12)
        self.week1_label.grid(column = 3, row = 2, padx = 5, pady = 5)

        self.sundayweek1client1 = StringVar()
        self.sunday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client1, width = 12)
        self.sunday_week1_client1.grid(column = 3, row = 3, padx = 5, pady = 5)

        self.sundayweek1client2 = StringVar()
        self.sunday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client2, width = 12)
        self.sunday_week1_client2.grid(column = 3, row = 4, padx = 5, pady = 5)

        self.sundayweek1client3 = StringVar()
        self.sunday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client3, width = 12)
        self.sunday_week1_client3.grid(column = 3, row = 5, padx = 5, pady = 5)

        self.sundayweek1client4 = StringVar()
        self.sunday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client4, width = 12)
        self.sunday_week1_client4.grid(column = 3, row = 6, padx = 5, pady = 5)

        self.sundayweek1client5 = StringVar()
        self.sunday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client5, width = 12)
        self.sunday_week1_client5.grid(column = 3, row = 7, padx = 5, pady = 5)

        self.sundayweek1client6 = StringVar()
        self.sunday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client6, width = 12)
        self.sunday_week1_client6.grid(column = 3, row = 8, padx = 5, pady = 5)

        self.sundayweek1client7 = StringVar()
        self.sunday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client7, width = 12)
        self.sunday_week1_client7.grid(column = 3, row = 9, padx = 5, pady = 5)

        self.sundayweek1client8 = StringVar()
        self.sunday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client8, width = 12)
        self.sunday_week1_client8.grid(column = 3, row = 10, padx = 5, pady = 5)

        self.sundayweek1client9 = StringVar()
        self.sunday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client9, width = 12)
        self.sunday_week1_client9.grid(column = 3, row = 11, padx = 5, pady = 5)

        self.sundayweek1client10 = StringVar()
        self.sunday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client10, width = 12)
        self.sunday_week1_client10.grid(column = 3, row = 12, padx = 5, pady = 5)

        self.sundayweek1client11 = StringVar()
        self.sunday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client11, width = 12)
        self.sunday_week1_client11.grid(column = 3, row = 13, padx = 5, pady = 5)

        self.sundayweek1client12 = StringVar()
        self.sunday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client12, width = 12)
        self.sunday_week1_client12.grid(column = 3, row = 14, padx = 5, pady = 5)

        self.sundayweek1client13 = StringVar()
        self.sunday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client13, width = 12)
        self.sunday_week1_client13.grid(column = 3, row = 15, padx = 5, pady = 5)

        self.sundayweek1client14 = StringVar()
        self.sunday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client14, width = 12)
        self.sunday_week1_client14.grid(column = 3, row = 16, padx = 5, pady = 5)

        self.sundayweek1client15 = StringVar()
        self.sunday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client15, width = 12)
        self.sunday_week1_client15.grid(column = 3, row = 17, padx = 5, pady = 5)

        self.sundayweek1client16 = StringVar()
        self.sunday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client16, width = 12)
        self.sunday_week1_client16.grid(column = 3, row = 18, padx = 5, pady = 5)

        self.sundayweek1client17 = StringVar()
        self.sunday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client17, width = 12)
        self.sunday_week1_client17.grid(column = 3, row = 19, padx = 5, pady = 5)

        self.sundayweek1client18 = StringVar()
        self.sunday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client18, width = 12)
        self.sunday_week1_client18.grid(column = 3, row = 20, padx = 5, pady = 5)

        self.sundayweek1client19 = StringVar()
        self.sunday_week1_client19= Entry(self.wrapper1frame, textvariable = self.sundayweek1client19, width = 12)
        self.sunday_week1_client19.grid(column = 3, row = 21, padx = 5, pady = 5)

        self.sundayweek1client20 = StringVar()
        self.sunday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.sundayweek1client20, width = 12)
        self.sunday_week1_client20.grid(column = 3, row = 22, padx = 5, pady = 5)

        self.mondayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.mondayweek1, width = 12)
        self.week1_label.grid(column = 4, row = 2, padx = 5, pady = 5)

        self.mondayweek1client1 = StringVar()
        self.monday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client1, width = 12)
        self.monday_week1_client1.grid(column = 4, row = 3, padx = 5, pady = 5)

        self.mondayweek1client2 = StringVar()
        self.monday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client2, width = 12)
        self.monday_week1_client2.grid(column = 4, row = 4, padx = 5, pady = 5)

        self.mondayweek1client3 = StringVar()
        self.monday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client3, width = 12)
        self.monday_week1_client3.grid(column = 4, row = 5, padx = 5, pady = 5)

        self.mondayweek1client4 = StringVar()
        self.monday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client4, width = 12)
        self.monday_week1_client4.grid(column = 4, row = 6, padx = 5, pady = 5)

        self.mondayweek1client5 = StringVar()
        self.monday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client5, width = 12)
        self.monday_week1_client5.grid(column = 4, row = 7, padx = 5, pady = 5)

        self.mondayweek1client6 = StringVar()
        self.monday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client6, width = 12)
        self.monday_week1_client6.grid(column = 4, row = 8, padx = 5, pady = 5)

        self.mondayweek1client7 = StringVar()
        self.monday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client7, width = 12)
        self.monday_week1_client7.grid(column = 4, row = 9, padx = 5, pady = 5)

        self.mondayweek1client8 = StringVar()
        self.monday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client8, width = 12)
        self.monday_week1_client8.grid(column = 4, row = 10, padx = 5, pady = 5)

        self.mondayweek1client9 = StringVar()
        self.monday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client9, width = 12)
        self.monday_week1_client9.grid(column = 4, row = 11, padx = 5, pady = 5)

        self.mondayweek1client10 = StringVar()
        self.monday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client10, width = 12)
        self.monday_week1_client10.grid(column = 4, row = 12, padx = 5, pady = 5)

        self.mondayweek1client11 = StringVar()
        self.monday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client11, width = 12)
        self.monday_week1_client11.grid(column = 4, row = 13, padx = 5, pady = 5)

        self.mondayweek1client12 = StringVar()
        self.monday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client12, width = 12)
        self.monday_week1_client12.grid(column = 4, row = 14, padx = 5, pady = 5)

        self.mondayweek1client13 = StringVar()
        self.monday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client13, width = 12)
        self.monday_week1_client13.grid(column = 4, row = 15, padx = 5, pady = 5)

        self.mondayweek1client14 = StringVar()
        self.monday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client14, width = 12)
        self.monday_week1_client14.grid(column = 4, row = 16, padx = 5, pady = 5)

        self.mondayweek1client15 = StringVar()
        self.monday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client15, width = 12)
        self.monday_week1_client15.grid(column = 4, row = 17, padx = 5, pady = 5)

        self.mondayweek1client16 = StringVar()
        self.monday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client16, width = 12)
        self.monday_week1_client16.grid(column = 4, row = 18, padx = 5, pady = 5)

        self.mondayweek1client17 = StringVar()
        self.monday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client17, width = 12)
        self.monday_week1_client17.grid(column = 4, row = 19, padx = 5, pady = 5)

        self.mondayweek1client18 = StringVar()
        self.monday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client18, width = 12)
        self.monday_week1_client18.grid(column = 4, row = 20, padx = 5, pady = 5)

        self.mondayweek1client19 = StringVar()
        self.monday_week1_client19= Entry(self.wrapper1frame, textvariable = self.mondayweek1client19, width = 12)
        self.monday_week1_client19.grid(column = 4, row = 21, padx = 5, pady = 5)

        self.mondayweek1client20 = StringVar()
        self.monday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.mondayweek1client20, width = 12)
        self.monday_week1_client20.grid(column = 4, row = 22, padx = 5, pady = 5)

        self.tuesdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1, width = 12)
        self.week1_label.grid(column = 5, row = 2, padx = 5, pady = 5)

        self.tuesdayweek1client1 = StringVar()
        self.tuesday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client1, width = 12)
        self.tuesday_week1_client1.grid(column = 5, row = 3, padx = 5, pady = 5)

        self.tuesdayweek1client2 = StringVar()
        self.tuesday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client2, width = 12)
        self.tuesday_week1_client2.grid(column = 5, row = 4, padx = 5, pady = 5)

        self.tuesdayweek1client3 = StringVar()
        self.tuesday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client3, width = 12)
        self.tuesday_week1_client3.grid(column = 5, row = 5, padx = 5, pady = 5)

        self.tuesdayweek1client4 = StringVar()
        self.tuesday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client4, width = 12)
        self.tuesday_week1_client4.grid(column = 5, row = 6, padx = 5, pady = 5)

        self.tuesdayweek1client5 = StringVar()
        self.tuesday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client5, width = 12)
        self.tuesday_week1_client5.grid(column = 5, row = 7, padx = 5, pady = 5)

        self.tuesdayweek1client6 = StringVar()
        self.tuesday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client6, width = 12)
        self.tuesday_week1_client6.grid(column = 5, row = 8, padx = 5, pady = 5)

        self.tuesdayweek1client7 = StringVar()
        self.tuesday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client7, width = 12)
        self.tuesday_week1_client7.grid(column = 5, row = 9, padx = 5, pady = 5)

        self.tuesdayweek1client8 = StringVar()
        self.tuesday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client8, width = 12)
        self.tuesday_week1_client8.grid(column = 5, row = 10, padx = 5, pady = 5)

        self.tuesdayweek1client9 = StringVar()
        self.tuesday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client9, width = 12)
        self.tuesday_week1_client9.grid(column = 5, row = 11, padx = 5, pady = 5)

        self.tuesdayweek1client10 = StringVar()
        self.tuesday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client10, width = 12)
        self.tuesday_week1_client10.grid(column = 5, row = 12, padx = 5, pady = 5)

        self.tuesdayweek1client11 = StringVar()
        self.tuesday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client11, width = 12)
        self.tuesday_week1_client11.grid(column = 5, row = 13, padx = 5, pady = 5)

        self.tuesdayweek1client12 = StringVar()
        self.tuesday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client12, width = 12)
        self.tuesday_week1_client12.grid(column = 5, row = 14, padx = 5, pady = 5)

        self.tuesdayweek1client13 = StringVar()
        self.tuesday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client13, width = 12)
        self.tuesday_week1_client13.grid(column = 5, row = 15, padx = 5, pady = 5)

        self.tuesdayweek1client14 = StringVar()
        self.tuesday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client14, width = 12)
        self.tuesday_week1_client14.grid(column = 5, row = 16, padx = 5, pady = 5)

        self.tuesdayweek1client15 = StringVar()
        self.tuesday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client15, width = 12)
        self.tuesday_week1_client15.grid(column = 5, row = 17, padx = 5, pady = 5)

        self.tuesdayweek1client16 = StringVar()
        self.tuesday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client16, width = 12)
        self.tuesday_week1_client16.grid(column = 5, row = 18, padx = 5, pady = 5)

        self.tuesdayweek1client17 = StringVar()
        self.tuesday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client17, width = 12)
        self.tuesday_week1_client17.grid(column = 5, row = 19, padx = 5, pady = 5)

        self.tuesdayweek1client18 = StringVar()
        self.tuesday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client18, width = 12)
        self.tuesday_week1_client18.grid(column = 5, row = 20, padx = 5, pady = 5)

        self.tuesdayweek1client19 = StringVar()
        self.tuesday_week1_client19= Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client19, width = 12)
        self.tuesday_week1_client19.grid(column = 5, row = 21, padx = 5, pady = 5)

        self.tuesdayweek1client20 = StringVar()
        self.tuesday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.tuesdayweek1client20, width = 12)
        self.tuesday_week1_client20.grid(column = 5, row = 22, padx = 5, pady = 5)

        self.wednesdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1, width = 12)
        self.week1_label.grid(column = 6, row = 2, padx = 5, pady = 5)

        self.wednesdayweek1client1 = StringVar()
        self.wednesday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client1, width = 12)
        self.wednesday_week1_client1.grid(column = 6, row = 3, padx = 5, pady = 5)

        self.wednesdayweek1client2 = StringVar()
        self.wednesday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client2, width = 12)
        self.wednesday_week1_client2.grid(column = 6, row = 4, padx = 5, pady = 5)

        self.wednesdayweek1client3 = StringVar()
        self.wednesday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client3, width = 12)
        self.wednesday_week1_client3.grid(column = 6, row = 5, padx = 5, pady = 5)

        self.wednesdayweek1client4 = StringVar()
        self.wednesday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client4, width = 12)
        self.wednesday_week1_client4.grid(column = 6, row = 6, padx = 5, pady = 5)

        self.wednesdayweek1client5 = StringVar()
        self.wednesday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client5, width = 12)
        self.wednesday_week1_client5.grid(column = 6, row = 7, padx = 5, pady = 5)

        self.wednesdayweek1client6 = StringVar()
        self.wednesday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client6, width = 12)
        self.wednesday_week1_client6.grid(column = 6, row = 8, padx = 5, pady = 5)

        self.wednesdayweek1client7 = StringVar()
        self.wednesday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client7, width = 12)
        self.wednesday_week1_client7.grid(column = 6, row = 9, padx = 5, pady = 5)

        self.wednesdayweek1client8 = StringVar()
        self.wednesday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client8, width = 12)
        self.wednesday_week1_client8.grid(column = 6, row = 10, padx = 5, pady = 5)

        self.wednesdayweek1client9 = StringVar()
        self.wednesday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client9, width = 12)
        self.wednesday_week1_client9.grid(column = 6, row = 11, padx = 5, pady = 5)

        self.wednesdayweek1client10 = StringVar()
        self.wednesday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client10, width = 12)
        self.wednesday_week1_client10.grid(column = 6, row = 12, padx = 5, pady = 5)

        self.wednesdayweek1client11 = StringVar()
        self.wednesday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client11, width = 12)
        self.wednesday_week1_client11.grid(column = 6, row = 13, padx = 5, pady = 5)

        self.wednesdayweek1client12 = StringVar()
        self.wednesday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client12, width = 12)
        self.wednesday_week1_client12.grid(column = 6, row = 14, padx = 5, pady = 5)

        self.wednesdayweek1client13 = StringVar()
        self.wednesday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client13, width = 12)
        self.wednesday_week1_client13.grid(column = 6, row = 15, padx = 5, pady = 5)

        self.wednesdayweek1client14 = StringVar()
        self.wednesday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client14, width = 12)
        self.wednesday_week1_client14.grid(column = 6, row = 16, padx = 5, pady = 5)

        self.wednesdayweek1client15 = StringVar()
        self.wednesday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client15, width = 12)
        self.wednesday_week1_client15.grid(column = 6, row = 17, padx = 5, pady = 5)

        self.wednesdayweek1client16 = StringVar()
        self.wednesday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client16, width = 12)
        self.wednesday_week1_client16.grid(column = 6, row = 18, padx = 5, pady = 5)

        self.wednesdayweek1client17 = StringVar()
        self.wednesday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client17, width = 12)
        self.wednesday_week1_client17.grid(column = 6, row = 19, padx = 5, pady = 5)

        self.wednesdayweek1client18 = StringVar()
        self.wednesday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client18, width = 12)
        self.wednesday_week1_client18.grid(column = 6, row = 20, padx = 5, pady = 5)

        self.wednesdayweek1client19 = StringVar()
        self.wednesday_week1_client19= Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client19, width = 12)
        self.wednesday_week1_client19.grid(column = 6, row = 21, padx = 5, pady = 5)

        self.wednesdayweek1client20 = StringVar()
        self.wednesday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.wednesdayweek1client20, width = 12)
        self.wednesday_week1_client20.grid(column = 6, row = 22, padx = 5, pady = 5)

        self.thursdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.thursdayweek1, width = 12)
        self.week1_label.grid(column = 7, row = 2, padx = 5, pady = 5)

        self.thursdayweek1client1 = StringVar()
        self.thursday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client1, width = 12)
        self.thursday_week1_client1.grid(column = 7, row = 3, padx = 5, pady = 5)

        self.thursdayweek1client2 = StringVar()
        self.thursday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client2, width = 12)
        self.thursday_week1_client2.grid(column = 7, row = 4, padx = 5, pady = 5)

        self.thursdayweek1client3 = StringVar()
        self.thursday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client3, width = 12)
        self.thursday_week1_client3.grid(column = 7, row = 5, padx = 5, pady = 5)

        self.thursdayweek1client4 = StringVar()
        self.thursday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client4, width = 12)
        self.thursday_week1_client4.grid(column = 7, row = 6, padx = 5, pady = 5)

        self.thursdayweek1client5 = StringVar()
        self.thursday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client5, width = 12)
        self.thursday_week1_client5.grid(column = 7, row = 7, padx = 5, pady = 5)

        self.thursdayweek1client6 = StringVar()
        self.thursday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client6, width = 12)
        self.thursday_week1_client6.grid(column = 7, row = 8, padx = 5, pady = 5)

        self.thursdayweek1client7 = StringVar()
        self.thursday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client7, width = 12)
        self.thursday_week1_client7.grid(column = 7, row = 9, padx = 5, pady = 5)

        self.thursdayweek1client8 = StringVar()
        self.thursday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client8, width = 12)
        self.thursday_week1_client8.grid(column = 7, row = 10, padx = 5, pady = 5)

        self.thursdayweek1client9 = StringVar()
        self.thursday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client9, width = 12)
        self.thursday_week1_client9.grid(column = 7, row = 11, padx = 5, pady = 5)

        self.thursdayweek1client10 = StringVar()
        self.thursday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client10, width = 12)
        self.thursday_week1_client10.grid(column = 7, row = 12, padx = 5, pady = 5)

        self.thursdayweek1client11 = StringVar()
        self.thursday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client11, width = 12)
        self.thursday_week1_client11.grid(column = 7, row = 13, padx = 5, pady = 5)

        self.thursdayweek1client12 = StringVar()
        self.thursday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client12, width = 12)
        self.thursday_week1_client12.grid(column = 7, row = 14, padx = 5, pady = 5)

        self.thursdayweek1client13 = StringVar()
        self.thursday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client13, width = 12)
        self.thursday_week1_client13.grid(column = 7, row = 15, padx = 5, pady = 5)

        self.thursdayweek1client14 = StringVar()
        self.thursday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client14, width = 12)
        self.thursday_week1_client14.grid(column = 7, row = 16, padx = 5, pady = 5)

        self.thursdayweek1client15 = StringVar()
        self.thursday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client15, width = 12)
        self.thursday_week1_client15.grid(column = 7, row = 17, padx = 5, pady = 5)

        self.thursdayweek1client16 = StringVar()
        self.thursday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client16, width = 12)
        self.thursday_week1_client16.grid(column = 7, row = 18, padx = 5, pady = 5)

        self.thursdayweek1client17 = StringVar()
        self.thursday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client17, width = 12)
        self.thursday_week1_client17.grid(column = 7, row = 19, padx = 5, pady = 5)

        self.thursdayweek1client18 = StringVar()
        self.thursday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client18, width = 12)
        self.thursday_week1_client18.grid(column = 7, row = 20, padx = 5, pady = 5)

        self.thursdayweek1client19 = StringVar()
        self.thursday_week1_client19= Entry(self.wrapper1frame, textvariable = self.thursdayweek1client19, width = 12)
        self.thursday_week1_client19.grid(column = 7, row = 21, padx = 5, pady = 5)

        self.thursdayweek1client20 = StringVar()
        self.thursday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.thursdayweek1client20, width = 12)
        self.thursday_week1_client20.grid(column = 7, row = 22, padx = 5, pady = 5)

        self.fridayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper1frame, textvariable = self.fridayweek1, width = 12)
        self.week1_label.grid(column = 8, row = 2, padx = 5, pady = 5)

        self.fridayweek1client1 = StringVar()
        self.friday_week1_client1 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client1, width = 12)
        self.friday_week1_client1.grid(column = 8, row = 3, padx = 5, pady = 5)

        self.fridayweek1client2 = StringVar()
        self.friday_week1_client2 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client2, width = 12)
        self.friday_week1_client2.grid(column = 8, row = 4, padx = 5, pady = 5)

        self.fridayweek1client3 = StringVar()
        self.friday_week1_client3 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client3, width = 12)
        self.friday_week1_client3.grid(column = 8, row = 5, padx = 5, pady = 5)

        self.fridayweek1client4 = StringVar()
        self.friday_week1_client4 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client4, width = 12)
        self.friday_week1_client4.grid(column = 8, row = 6, padx = 5, pady = 5)

        self.fridayweek1client5 = StringVar()
        self.friday_week1_client5 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client5, width = 12)
        self.friday_week1_client5.grid(column = 8, row = 7, padx = 5, pady = 5)

        self.fridayweek1client6 = StringVar()
        self.friday_week1_client6 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client6, width = 12)
        self.friday_week1_client6.grid(column = 8, row = 8, padx = 5, pady = 5)

        self.fridayweek1client7 = StringVar()
        self.friday_week1_client7 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client7, width = 12)
        self.friday_week1_client7.grid(column = 8, row = 9, padx = 5, pady = 5)

        self.fridayweek1client8 = StringVar()
        self.friday_week1_client8 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client8, width = 12)
        self.friday_week1_client8.grid(column = 8, row = 10, padx = 5, pady = 5)

        self.fridayweek1client9 = StringVar()
        self.friday_week1_client9 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client9, width = 12)
        self.friday_week1_client9.grid(column = 8, row = 11, padx = 5, pady = 5)

        self.fridayweek1client10 = StringVar()
        self.friday_week1_client10 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client10, width = 12)
        self.friday_week1_client10.grid(column = 8, row = 12, padx = 5, pady = 5)

        self.fridayweek1client11 = StringVar()
        self.friday_week1_client11 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client11, width = 12)
        self.friday_week1_client11.grid(column = 8, row = 13, padx = 5, pady = 5)

        self.fridayweek1client12 = StringVar()
        self.friday_week1_client12 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client12, width = 12)
        self.friday_week1_client12.grid(column = 8, row = 14, padx = 5, pady = 5)

        self.fridayweek1client13 = StringVar()
        self.friday_week1_client13 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client13, width = 12)
        self.friday_week1_client13.grid(column = 8, row = 15, padx = 5, pady = 5)

        self.fridayweek1client14 = StringVar()
        self.friday_week1_client14 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client14, width = 12)
        self.friday_week1_client14.grid(column = 8, row = 16, padx = 5, pady = 5)

        self.fridayweek1client15 = StringVar()
        self.friday_week1_client15 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client15, width = 12)
        self.friday_week1_client15.grid(column = 8, row = 17, padx = 5, pady = 5)

        self.fridayweek1client16 = StringVar()
        self.friday_week1_client16 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client16, width = 12)
        self.friday_week1_client16.grid(column = 8, row = 18, padx = 5, pady = 5)

        self.fridayweek1client17 = StringVar()
        self.friday_week1_client17 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client17, width = 12)
        self.friday_week1_client17.grid(column = 8, row = 19, padx = 5, pady = 5)

        self.fridayweek1client18 = StringVar()
        self.friday_week1_client18 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client18, width = 12)
        self.friday_week1_client18.grid(column = 8, row = 20, padx = 5, pady = 5)

        self.fridayweek1client19 = StringVar()
        self.friday_week1_client19= Entry(self.wrapper1frame, textvariable = self.fridayweek1client19, width = 12)
        self.friday_week1_client19.grid(column = 8, row = 21, padx = 5, pady = 5)

        self.fridayweek1client20 = StringVar()
        self.friday_week1_client20 = Entry(self.wrapper1frame, textvariable = self.fridayweek1client20, width = 12)
        self.friday_week1_client20.grid(column = 8, row = 22, padx = 5, pady = 5)

        #Client 1 field
        self.notes_client1 = StringVar()
        self.notes_client1_selection = Entry(self.wrapper1frame, textvariable = self.notes_client1, width = 12)
        self.notes_client1_selection.grid(column = 9, row = 3, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        self.notes_client2 = StringVar()
        self.notes_client2_selection = Entry(self.wrapper1frame, textvariable = self.notes_client2, width = 12)
        self.notes_client2_selection.grid(column = 9, row = 4, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        self.notes_client3 = StringVar()
        self.notes_client3_selection = Entry(self.wrapper1frame, textvariable = self.notes_client3, width = 12)
        self.notes_client3_selection.grid(column = 9, row = 5, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        self.notes_client4 = StringVar()
        self.notes_client4_selection = Entry(self.wrapper1frame, textvariable = self.notes_client4, width = 12)
        self.notes_client4_selection.grid(column = 9, row = 6, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        self.notes_client5 = StringVar()
        self.notes_client5_selection = Entry(self.wrapper1frame, textvariable = self.notes_client5, width = 12)
        self.notes_client5_selection.grid(column = 9, row = 7, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        self.notes_client6 = StringVar()
        self.notes_client6_selection = Entry(self.wrapper1frame, textvariable = self.notes_client6, width = 12)
        self.notes_client6_selection.grid(column = 9, row = 8, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        self.notes_client7 = StringVar()
        self.notes_client7_selection = Entry(self.wrapper1frame, textvariable = self.notes_client7, width = 12)
        self.notes_client7_selection.grid(column = 9, row = 9, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        self.notes_client8 = StringVar()
        self.notes_client8_selection = Entry(self.wrapper1frame, textvariable = self.notes_client8, width = 12)
        self.notes_client8_selection.grid(column = 9, row = 10, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        self.notes_client9 = StringVar()
        self.notes_client9_selection = Entry(self.wrapper1frame, textvariable = self.notes_client9, width = 12)
        self.notes_client9_selection.grid(column = 9, row = 11, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        self.notes_client10 = StringVar()
        self.notes_client10_selection = Entry(self.wrapper1frame, textvariable = self.notes_client10, width = 12)
        self.notes_client10_selection.grid(column = 9, row = 12, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        self.notes_client11 = StringVar()
        self.notes_client11_selection = Entry(self.wrapper1frame, textvariable = self.notes_client11, width = 12)
        self.notes_client11_selection.grid(column = 9, row = 13, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        self.notes_client12 = StringVar()
        self.notes_client12_selection = Entry(self.wrapper1frame, textvariable = self.notes_client12, width = 12)
        self.notes_client12_selection.grid(column = 9, row = 14, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        self.notes_client13 = StringVar()
        self.notes_client13_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client13_selection.grid(column = 9, row = 15, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        self.notes_client14 = StringVar()
        self.notes_client14_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client14_selection.grid(column = 9, row = 16, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        self.notes_client15 = StringVar()
        self.notes_client15_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client15_selection.grid(column = 9, row = 17, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        self.notes_client16 = StringVar()
        self.notes_client16_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client16_selection.grid(column = 9, row = 18, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        self.notes_client17 = StringVar()
        self.notes_client17_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client17_selection.grid(column = 9, row = 19, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        self.notes_client18 = StringVar()
        self.notes_client18_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client18_selection.grid(column = 9, row = 20, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        self.notes_client19 = StringVar()
        self.notes_client19_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client19_selection.grid(column = 9, row = 21, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        self.notes_client20 = StringVar()
        self.notes_client20_selection = Entry(self.wrapper1frame, textvariable = self.notes_client13, width = 12)
        self.notes_client20_selection.grid(column = 9, row = 22, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper1frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 22, sticky = "we", padx = 5, pady = 5)

        #Client 1 field
        self.engagementcode_client1 = StringVar()
        self.engagementcode_client1_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client1, width = 12)
        self.engagementcode_client1_selection.grid(column = 0, row = 3, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        self.engagementcode_client2 = StringVar()
        self.engagementcode_client2_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client2, width = 12)
        self.engagementcode_client2_selection.grid(column = 0, row = 4, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        self.engagementcode_client3 = StringVar()
        self.engagementcode_client3_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client3, width = 12)
        self.engagementcode_client3_selection.grid(column = 0, row = 5, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        self.engagementcode_client4 = StringVar()
        self.engagementcode_client4_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client4, width = 12)
        self.engagementcode_client4_selection.grid(column = 0, row = 6, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        self.engagementcode_client5 = StringVar()
        self.engagementcode_client5_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client5, width = 12)
        self.engagementcode_client5_selection.grid(column = 0, row = 7, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        self.engagementcode_client6 = StringVar()
        self.engagementcode_client6_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client6, width = 12)
        self.engagementcode_client6_selection.grid(column = 0, row = 8, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        self.engagementcode_client7 = StringVar()
        self.engagementcode_client7_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client7, width = 12)
        self.engagementcode_client7_selection.grid(column = 0, row = 9, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        self.engagementcode_client8 = StringVar()
        self.engagementcode_client8_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client8, width = 12)
        self.engagementcode_client8_selection.grid(column = 0, row = 10, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        self.engagementcode_client9 = StringVar()
        self.engagementcode_client9_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client9, width = 12)
        self.engagementcode_client9_selection.grid(column = 0, row = 11, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        self.engagementcode_client10 = StringVar()
        self.engagementcode_client10_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client10, width = 12)
        self.engagementcode_client10_selection.grid(column = 0, row = 12, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        self.engagementcode_client11 = StringVar()
        self.engagementcode_client11_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client11, width = 12)
        self.engagementcode_client11_selection.grid(column = 0, row = 13, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        self.engagementcode_client12 = StringVar()
        self.engagementcode_client12_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client12, width = 12)
        self.engagementcode_client12_selection.grid(column = 0, row = 14, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        self.engagementcode_client13 = StringVar()
        self.engagementcode_client13_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client13_selection.grid(column = 0, row = 15, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        self.engagementcode_client14 = StringVar()
        self.engagementcode_client14_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client14_selection.grid(column = 0, row = 16, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        self.engagementcode_client15 = StringVar()
        self.engagementcode_client15_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client15_selection.grid(column = 0, row = 17, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        self.engagementcode_client16 = StringVar()
        self.engagementcode_client16_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client16_selection.grid(column = 0, row = 18, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        self.engagementcode_client17 = StringVar()
        self.engagementcode_client17_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client17_selection.grid(column = 0, row = 19, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        self.engagementcode_client18 = StringVar()
        self.engagementcode_client18_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client18_selection.grid(column = 0, row = 20, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        self.engagementcode_client19 = StringVar()
        self.engagementcode_client19_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client19_selection.grid(column = 0, row = 21, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        self.engagementcode_client20 = StringVar()
        self.engagementcode_client20_selection = Entry(self.wrapper2frame, textvariable = self.engagementcode_client13, width = 12)
        self.engagementcode_client20_selection.grid(column = 0, row = 22, columnspan = 1)

        self.engagementcode_client1_search = Button(self.wrapper2frame, image = self.search_icon_resize)
        self.engagementcode_client1_search.grid(column = 1, row = 22, sticky = "we", padx = 5, pady = 5)

        #Weekday hours field example
        self.saturdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.saturdayweek1, width = 12)
        self.week1_label.grid(column = 2, row = 2, padx = 5, pady = 5)

        self.saturdayweek1client1 = StringVar()
        self.saturday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client1, width = 12)
        self.saturday_week1_client1.grid(column = 2, row = 3, padx = 5, pady = 5)

        self.saturdayweek1client2 = StringVar()
        self.saturday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client2, width = 12)
        self.saturday_week1_client2.grid(column = 2, row = 4, padx = 5, pady = 5)

        self.saturdayweek1client3 = StringVar()
        self.saturday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client3, width = 12)
        self.saturday_week1_client3.grid(column = 2, row = 5, padx = 5, pady = 5)

        self.saturdayweek1client4 = StringVar()
        self.saturday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client4, width = 12)
        self.saturday_week1_client4.grid(column = 2, row = 6, padx = 5, pady = 5)

        self.saturdayweek1client5 = StringVar()
        self.saturday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client5, width = 12)
        self.saturday_week1_client5.grid(column = 2, row = 7, padx = 5, pady = 5)

        self.saturdayweek1client6 = StringVar()
        self.saturday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client6, width = 12)
        self.saturday_week1_client6.grid(column = 2, row = 8, padx = 5, pady = 5)

        self.saturdayweek1client7 = StringVar()
        self.saturday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client7, width = 12)
        self.saturday_week1_client7.grid(column = 2, row = 9, padx = 5, pady = 5)

        self.saturdayweek1client8 = StringVar()
        self.saturday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client8, width = 12)
        self.saturday_week1_client8.grid(column = 2, row = 10, padx = 5, pady = 5)

        self.saturdayweek1client9 = StringVar()
        self.saturday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client9, width = 12)
        self.saturday_week1_client9.grid(column = 2, row = 11, padx = 5, pady = 5)

        self.saturdayweek1client10 = StringVar()
        self.saturday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client10, width = 12)
        self.saturday_week1_client10.grid(column = 2, row = 12, padx = 5, pady = 5)

        self.saturdayweek1client11 = StringVar()
        self.saturday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client11, width = 12)
        self.saturday_week1_client11.grid(column = 2, row = 13, padx = 5, pady = 5)

        self.saturdayweek1client12 = StringVar()
        self.saturday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client12, width = 12)
        self.saturday_week1_client12.grid(column = 2, row = 14, padx = 5, pady = 5)

        self.saturdayweek1client13 = StringVar()
        self.saturday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client13, width = 12)
        self.saturday_week1_client13.grid(column = 2, row = 15, padx = 5, pady = 5)

        self.saturdayweek1client14 = StringVar()
        self.saturday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client14, width = 12)
        self.saturday_week1_client14.grid(column = 2, row = 16, padx = 5, pady = 5)

        self.saturdayweek1client15 = StringVar()
        self.saturday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client15, width = 12)
        self.saturday_week1_client15.grid(column = 2, row = 17, padx = 5, pady = 5)

        self.saturdayweek1client16 = StringVar()
        self.saturday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client16, width = 12)
        self.saturday_week1_client16.grid(column = 2, row = 18, padx = 5, pady = 5)

        self.saturdayweek1client17 = StringVar()
        self.saturday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client17, width = 12)
        self.saturday_week1_client17.grid(column = 2, row = 19, padx = 5, pady = 5)

        self.saturdayweek1client18 = StringVar()
        self.saturday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client18, width = 12)
        self.saturday_week1_client18.grid(column = 2, row = 20, padx = 5, pady = 5)

        self.saturdayweek1client19 = StringVar()
        self.saturday_week1_client19= Entry(self.wrapper2frame, textvariable = self.saturdayweek1client19, width = 12)
        self.saturday_week1_client19.grid(column = 2, row = 21, padx = 5, pady = 5)

        self.saturdayweek1client20 = StringVar()
        self.saturday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.saturdayweek1client20, width = 12)
        self.saturday_week1_client20.grid(column = 2, row = 22, padx = 5, pady = 5)

        self.sundayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.sundayweek1, width = 12)
        self.week1_label.grid(column = 3, row = 2, padx = 5, pady = 5)

        self.sundayweek1client1 = StringVar()
        self.sunday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client1, width = 12)
        self.sunday_week1_client1.grid(column = 3, row = 3, padx = 5, pady = 5)

        self.sundayweek1client2 = StringVar()
        self.sunday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client2, width = 12)
        self.sunday_week1_client2.grid(column = 3, row = 4, padx = 5, pady = 5)

        self.sundayweek1client3 = StringVar()
        self.sunday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client3, width = 12)
        self.sunday_week1_client3.grid(column = 3, row = 5, padx = 5, pady = 5)

        self.sundayweek1client4 = StringVar()
        self.sunday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client4, width = 12)
        self.sunday_week1_client4.grid(column = 3, row = 6, padx = 5, pady = 5)

        self.sundayweek1client5 = StringVar()
        self.sunday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client5, width = 12)
        self.sunday_week1_client5.grid(column = 3, row = 7, padx = 5, pady = 5)

        self.sundayweek1client6 = StringVar()
        self.sunday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client6, width = 12)
        self.sunday_week1_client6.grid(column = 3, row = 8, padx = 5, pady = 5)

        self.sundayweek1client7 = StringVar()
        self.sunday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client7, width = 12)
        self.sunday_week1_client7.grid(column = 3, row = 9, padx = 5, pady = 5)

        self.sundayweek1client8 = StringVar()
        self.sunday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client8, width = 12)
        self.sunday_week1_client8.grid(column = 3, row = 10, padx = 5, pady = 5)

        self.sundayweek1client9 = StringVar()
        self.sunday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client9, width = 12)
        self.sunday_week1_client9.grid(column = 3, row = 11, padx = 5, pady = 5)

        self.sundayweek1client10 = StringVar()
        self.sunday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client10, width = 12)
        self.sunday_week1_client10.grid(column = 3, row = 12, padx = 5, pady = 5)

        self.sundayweek1client11 = StringVar()
        self.sunday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client11, width = 12)
        self.sunday_week1_client11.grid(column = 3, row = 13, padx = 5, pady = 5)

        self.sundayweek1client12 = StringVar()
        self.sunday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client12, width = 12)
        self.sunday_week1_client12.grid(column = 3, row = 14, padx = 5, pady = 5)

        self.sundayweek1client13 = StringVar()
        self.sunday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client13, width = 12)
        self.sunday_week1_client13.grid(column = 3, row = 15, padx = 5, pady = 5)

        self.sundayweek1client14 = StringVar()
        self.sunday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client14, width = 12)
        self.sunday_week1_client14.grid(column = 3, row = 16, padx = 5, pady = 5)

        self.sundayweek1client15 = StringVar()
        self.sunday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client15, width = 12)
        self.sunday_week1_client15.grid(column = 3, row = 17, padx = 5, pady = 5)

        self.sundayweek1client16 = StringVar()
        self.sunday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client16, width = 12)
        self.sunday_week1_client16.grid(column = 3, row = 18, padx = 5, pady = 5)

        self.sundayweek1client17 = StringVar()
        self.sunday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client17, width = 12)
        self.sunday_week1_client17.grid(column = 3, row = 19, padx = 5, pady = 5)

        self.sundayweek1client18 = StringVar()
        self.sunday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client18, width = 12)
        self.sunday_week1_client18.grid(column = 3, row = 20, padx = 5, pady = 5)

        self.sundayweek1client19 = StringVar()
        self.sunday_week1_client19= Entry(self.wrapper2frame, textvariable = self.sundayweek1client19, width = 12)
        self.sunday_week1_client19.grid(column = 3, row = 21, padx = 5, pady = 5)

        self.sundayweek1client20 = StringVar()
        self.sunday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.sundayweek1client20, width = 12)
        self.sunday_week1_client20.grid(column = 3, row = 22, padx = 5, pady = 5)

        self.mondayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.mondayweek1, width = 12)
        self.week1_label.grid(column = 4, row = 2, padx = 5, pady = 5)

        self.mondayweek1client1 = StringVar()
        self.monday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client1, width = 12)
        self.monday_week1_client1.grid(column = 4, row = 3, padx = 5, pady = 5)

        self.mondayweek1client2 = StringVar()
        self.monday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client2, width = 12)
        self.monday_week1_client2.grid(column = 4, row = 4, padx = 5, pady = 5)

        self.mondayweek1client3 = StringVar()
        self.monday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client3, width = 12)
        self.monday_week1_client3.grid(column = 4, row = 5, padx = 5, pady = 5)

        self.mondayweek1client4 = StringVar()
        self.monday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client4, width = 12)
        self.monday_week1_client4.grid(column = 4, row = 6, padx = 5, pady = 5)

        self.mondayweek1client5 = StringVar()
        self.monday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client5, width = 12)
        self.monday_week1_client5.grid(column = 4, row = 7, padx = 5, pady = 5)

        self.mondayweek1client6 = StringVar()
        self.monday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client6, width = 12)
        self.monday_week1_client6.grid(column = 4, row = 8, padx = 5, pady = 5)

        self.mondayweek1client7 = StringVar()
        self.monday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client7, width = 12)
        self.monday_week1_client7.grid(column = 4, row = 9, padx = 5, pady = 5)

        self.mondayweek1client8 = StringVar()
        self.monday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client8, width = 12)
        self.monday_week1_client8.grid(column = 4, row = 10, padx = 5, pady = 5)

        self.mondayweek1client9 = StringVar()
        self.monday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client9, width = 12)
        self.monday_week1_client9.grid(column = 4, row = 11, padx = 5, pady = 5)

        self.mondayweek1client10 = StringVar()
        self.monday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client10, width = 12)
        self.monday_week1_client10.grid(column = 4, row = 12, padx = 5, pady = 5)

        self.mondayweek1client11 = StringVar()
        self.monday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client11, width = 12)
        self.monday_week1_client11.grid(column = 4, row = 13, padx = 5, pady = 5)

        self.mondayweek1client12 = StringVar()
        self.monday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client12, width = 12)
        self.monday_week1_client12.grid(column = 4, row = 14, padx = 5, pady = 5)

        self.mondayweek1client13 = StringVar()
        self.monday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client13, width = 12)
        self.monday_week1_client13.grid(column = 4, row = 15, padx = 5, pady = 5)

        self.mondayweek1client14 = StringVar()
        self.monday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client14, width = 12)
        self.monday_week1_client14.grid(column = 4, row = 16, padx = 5, pady = 5)

        self.mondayweek1client15 = StringVar()
        self.monday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client15, width = 12)
        self.monday_week1_client15.grid(column = 4, row = 17, padx = 5, pady = 5)

        self.mondayweek1client16 = StringVar()
        self.monday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client16, width = 12)
        self.monday_week1_client16.grid(column = 4, row = 18, padx = 5, pady = 5)

        self.mondayweek1client17 = StringVar()
        self.monday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client17, width = 12)
        self.monday_week1_client17.grid(column = 4, row = 19, padx = 5, pady = 5)

        self.mondayweek1client18 = StringVar()
        self.monday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client18, width = 12)
        self.monday_week1_client18.grid(column = 4, row = 20, padx = 5, pady = 5)

        self.mondayweek1client19 = StringVar()
        self.monday_week1_client19= Entry(self.wrapper2frame, textvariable = self.mondayweek1client19, width = 12)
        self.monday_week1_client19.grid(column = 4, row = 21, padx = 5, pady = 5)

        self.mondayweek1client20 = StringVar()
        self.monday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.mondayweek1client20, width = 12)
        self.monday_week1_client20.grid(column = 4, row = 22, padx = 5, pady = 5)

        self.tuesdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1, width = 12)
        self.week1_label.grid(column = 5, row = 2, padx = 5, pady = 5)

        self.tuesdayweek1client1 = StringVar()
        self.tuesday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client1, width = 12)
        self.tuesday_week1_client1.grid(column = 5, row = 3, padx = 5, pady = 5)

        self.tuesdayweek1client2 = StringVar()
        self.tuesday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client2, width = 12)
        self.tuesday_week1_client2.grid(column = 5, row = 4, padx = 5, pady = 5)

        self.tuesdayweek1client3 = StringVar()
        self.tuesday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client3, width = 12)
        self.tuesday_week1_client3.grid(column = 5, row = 5, padx = 5, pady = 5)

        self.tuesdayweek1client4 = StringVar()
        self.tuesday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client4, width = 12)
        self.tuesday_week1_client4.grid(column = 5, row = 6, padx = 5, pady = 5)

        self.tuesdayweek1client5 = StringVar()
        self.tuesday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client5, width = 12)
        self.tuesday_week1_client5.grid(column = 5, row = 7, padx = 5, pady = 5)

        self.tuesdayweek1client6 = StringVar()
        self.tuesday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client6, width = 12)
        self.tuesday_week1_client6.grid(column = 5, row = 8, padx = 5, pady = 5)

        self.tuesdayweek1client7 = StringVar()
        self.tuesday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client7, width = 12)
        self.tuesday_week1_client7.grid(column = 5, row = 9, padx = 5, pady = 5)

        self.tuesdayweek1client8 = StringVar()
        self.tuesday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client8, width = 12)
        self.tuesday_week1_client8.grid(column = 5, row = 10, padx = 5, pady = 5)

        self.tuesdayweek1client9 = StringVar()
        self.tuesday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client9, width = 12)
        self.tuesday_week1_client9.grid(column = 5, row = 11, padx = 5, pady = 5)

        self.tuesdayweek1client10 = StringVar()
        self.tuesday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client10, width = 12)
        self.tuesday_week1_client10.grid(column = 5, row = 12, padx = 5, pady = 5)

        self.tuesdayweek1client11 = StringVar()
        self.tuesday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client11, width = 12)
        self.tuesday_week1_client11.grid(column = 5, row = 13, padx = 5, pady = 5)

        self.tuesdayweek1client12 = StringVar()
        self.tuesday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client12, width = 12)
        self.tuesday_week1_client12.grid(column = 5, row = 14, padx = 5, pady = 5)

        self.tuesdayweek1client13 = StringVar()
        self.tuesday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client13, width = 12)
        self.tuesday_week1_client13.grid(column = 5, row = 15, padx = 5, pady = 5)

        self.tuesdayweek1client14 = StringVar()
        self.tuesday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client14, width = 12)
        self.tuesday_week1_client14.grid(column = 5, row = 16, padx = 5, pady = 5)

        self.tuesdayweek1client15 = StringVar()
        self.tuesday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client15, width = 12)
        self.tuesday_week1_client15.grid(column = 5, row = 17, padx = 5, pady = 5)

        self.tuesdayweek1client16 = StringVar()
        self.tuesday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client16, width = 12)
        self.tuesday_week1_client16.grid(column = 5, row = 18, padx = 5, pady = 5)

        self.tuesdayweek1client17 = StringVar()
        self.tuesday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client17, width = 12)
        self.tuesday_week1_client17.grid(column = 5, row = 19, padx = 5, pady = 5)

        self.tuesdayweek1client18 = StringVar()
        self.tuesday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client18, width = 12)
        self.tuesday_week1_client18.grid(column = 5, row = 20, padx = 5, pady = 5)

        self.tuesdayweek1client19 = StringVar()
        self.tuesday_week1_client19= Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client19, width = 12)
        self.tuesday_week1_client19.grid(column = 5, row = 21, padx = 5, pady = 5)

        self.tuesdayweek1client20 = StringVar()
        self.tuesday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.tuesdayweek1client20, width = 12)
        self.tuesday_week1_client20.grid(column = 5, row = 22, padx = 5, pady = 5)

        self.wednesdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1, width = 12)
        self.week1_label.grid(column = 6, row = 2, padx = 5, pady = 5)

        self.wednesdayweek1client1 = StringVar()
        self.wednesday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client1, width = 12)
        self.wednesday_week1_client1.grid(column = 6, row = 3, padx = 5, pady = 5)

        self.wednesdayweek1client2 = StringVar()
        self.wednesday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client2, width = 12)
        self.wednesday_week1_client2.grid(column = 6, row = 4, padx = 5, pady = 5)

        self.wednesdayweek1client3 = StringVar()
        self.wednesday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client3, width = 12)
        self.wednesday_week1_client3.grid(column = 6, row = 5, padx = 5, pady = 5)

        self.wednesdayweek1client4 = StringVar()
        self.wednesday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client4, width = 12)
        self.wednesday_week1_client4.grid(column = 6, row = 6, padx = 5, pady = 5)

        self.wednesdayweek1client5 = StringVar()
        self.wednesday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client5, width = 12)
        self.wednesday_week1_client5.grid(column = 6, row = 7, padx = 5, pady = 5)

        self.wednesdayweek1client6 = StringVar()
        self.wednesday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client6, width = 12)
        self.wednesday_week1_client6.grid(column = 6, row = 8, padx = 5, pady = 5)

        self.wednesdayweek1client7 = StringVar()
        self.wednesday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client7, width = 12)
        self.wednesday_week1_client7.grid(column = 6, row = 9, padx = 5, pady = 5)

        self.wednesdayweek1client8 = StringVar()
        self.wednesday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client8, width = 12)
        self.wednesday_week1_client8.grid(column = 6, row = 10, padx = 5, pady = 5)

        self.wednesdayweek1client9 = StringVar()
        self.wednesday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client9, width = 12)
        self.wednesday_week1_client9.grid(column = 6, row = 11, padx = 5, pady = 5)

        self.wednesdayweek1client10 = StringVar()
        self.wednesday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client10, width = 12)
        self.wednesday_week1_client10.grid(column = 6, row = 12, padx = 5, pady = 5)

        self.wednesdayweek1client11 = StringVar()
        self.wednesday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client11, width = 12)
        self.wednesday_week1_client11.grid(column = 6, row = 13, padx = 5, pady = 5)

        self.wednesdayweek1client12 = StringVar()
        self.wednesday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client12, width = 12)
        self.wednesday_week1_client12.grid(column = 6, row = 14, padx = 5, pady = 5)

        self.wednesdayweek1client13 = StringVar()
        self.wednesday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client13, width = 12)
        self.wednesday_week1_client13.grid(column = 6, row = 15, padx = 5, pady = 5)

        self.wednesdayweek1client14 = StringVar()
        self.wednesday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client14, width = 12)
        self.wednesday_week1_client14.grid(column = 6, row = 16, padx = 5, pady = 5)

        self.wednesdayweek1client15 = StringVar()
        self.wednesday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client15, width = 12)
        self.wednesday_week1_client15.grid(column = 6, row = 17, padx = 5, pady = 5)

        self.wednesdayweek1client16 = StringVar()
        self.wednesday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client16, width = 12)
        self.wednesday_week1_client16.grid(column = 6, row = 18, padx = 5, pady = 5)

        self.wednesdayweek1client17 = StringVar()
        self.wednesday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client17, width = 12)
        self.wednesday_week1_client17.grid(column = 6, row = 19, padx = 5, pady = 5)

        self.wednesdayweek1client18 = StringVar()
        self.wednesday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client18, width = 12)
        self.wednesday_week1_client18.grid(column = 6, row = 20, padx = 5, pady = 5)

        self.wednesdayweek1client19 = StringVar()
        self.wednesday_week1_client19= Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client19, width = 12)
        self.wednesday_week1_client19.grid(column = 6, row = 21, padx = 5, pady = 5)

        self.wednesdayweek1client20 = StringVar()
        self.wednesday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.wednesdayweek1client20, width = 12)
        self.wednesday_week1_client20.grid(column = 6, row = 22, padx = 5, pady = 5)

        self.thursdayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.thursdayweek1, width = 12)
        self.week1_label.grid(column = 7, row = 2, padx = 5, pady = 5)

        self.thursdayweek1client1 = StringVar()
        self.thursday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client1, width = 12)
        self.thursday_week1_client1.grid(column = 7, row = 3, padx = 5, pady = 5)

        self.thursdayweek1client2 = StringVar()
        self.thursday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client2, width = 12)
        self.thursday_week1_client2.grid(column = 7, row = 4, padx = 5, pady = 5)

        self.thursdayweek1client3 = StringVar()
        self.thursday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client3, width = 12)
        self.thursday_week1_client3.grid(column = 7, row = 5, padx = 5, pady = 5)

        self.thursdayweek1client4 = StringVar()
        self.thursday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client4, width = 12)
        self.thursday_week1_client4.grid(column = 7, row = 6, padx = 5, pady = 5)

        self.thursdayweek1client5 = StringVar()
        self.thursday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client5, width = 12)
        self.thursday_week1_client5.grid(column = 7, row = 7, padx = 5, pady = 5)

        self.thursdayweek1client6 = StringVar()
        self.thursday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client6, width = 12)
        self.thursday_week1_client6.grid(column = 7, row = 8, padx = 5, pady = 5)

        self.thursdayweek1client7 = StringVar()
        self.thursday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client7, width = 12)
        self.thursday_week1_client7.grid(column = 7, row = 9, padx = 5, pady = 5)

        self.thursdayweek1client8 = StringVar()
        self.thursday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client8, width = 12)
        self.thursday_week1_client8.grid(column = 7, row = 10, padx = 5, pady = 5)

        self.thursdayweek1client9 = StringVar()
        self.thursday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client9, width = 12)
        self.thursday_week1_client9.grid(column = 7, row = 11, padx = 5, pady = 5)

        self.thursdayweek1client10 = StringVar()
        self.thursday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client10, width = 12)
        self.thursday_week1_client10.grid(column = 7, row = 12, padx = 5, pady = 5)

        self.thursdayweek1client11 = StringVar()
        self.thursday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client11, width = 12)
        self.thursday_week1_client11.grid(column = 7, row = 13, padx = 5, pady = 5)

        self.thursdayweek1client12 = StringVar()
        self.thursday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client12, width = 12)
        self.thursday_week1_client12.grid(column = 7, row = 14, padx = 5, pady = 5)

        self.thursdayweek1client13 = StringVar()
        self.thursday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client13, width = 12)
        self.thursday_week1_client13.grid(column = 7, row = 15, padx = 5, pady = 5)

        self.thursdayweek1client14 = StringVar()
        self.thursday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client14, width = 12)
        self.thursday_week1_client14.grid(column = 7, row = 16, padx = 5, pady = 5)

        self.thursdayweek1client15 = StringVar()
        self.thursday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client15, width = 12)
        self.thursday_week1_client15.grid(column = 7, row = 17, padx = 5, pady = 5)

        self.thursdayweek1client16 = StringVar()
        self.thursday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client16, width = 12)
        self.thursday_week1_client16.grid(column = 7, row = 18, padx = 5, pady = 5)

        self.thursdayweek1client17 = StringVar()
        self.thursday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client17, width = 12)
        self.thursday_week1_client17.grid(column = 7, row = 19, padx = 5, pady = 5)

        self.thursdayweek1client18 = StringVar()
        self.thursday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client18, width = 12)
        self.thursday_week1_client18.grid(column = 7, row = 20, padx = 5, pady = 5)

        self.thursdayweek1client19 = StringVar()
        self.thursday_week1_client19= Entry(self.wrapper2frame, textvariable = self.thursdayweek1client19, width = 12)
        self.thursday_week1_client19.grid(column = 7, row = 21, padx = 5, pady = 5)

        self.thursdayweek1client20 = StringVar()
        self.thursday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.thursdayweek1client20, width = 12)
        self.thursday_week1_client20.grid(column = 7, row = 22, padx = 5, pady = 5)

        self.fridayweek1 = StringVar()
        self.week1_label = Entry(self.wrapper2frame, textvariable = self.fridayweek1, width = 12)
        self.week1_label.grid(column = 8, row = 2, padx = 5, pady = 5)

        self.fridayweek1client1 = StringVar()
        self.friday_week1_client1 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client1, width = 12)
        self.friday_week1_client1.grid(column = 8, row = 3, padx = 5, pady = 5)

        self.fridayweek1client2 = StringVar()
        self.friday_week1_client2 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client2, width = 12)
        self.friday_week1_client2.grid(column = 8, row = 4, padx = 5, pady = 5)

        self.fridayweek1client3 = StringVar()
        self.friday_week1_client3 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client3, width = 12)
        self.friday_week1_client3.grid(column = 8, row = 5, padx = 5, pady = 5)

        self.fridayweek1client4 = StringVar()
        self.friday_week1_client4 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client4, width = 12)
        self.friday_week1_client4.grid(column = 8, row = 6, padx = 5, pady = 5)

        self.fridayweek1client5 = StringVar()
        self.friday_week1_client5 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client5, width = 12)
        self.friday_week1_client5.grid(column = 8, row = 7, padx = 5, pady = 5)

        self.fridayweek1client6 = StringVar()
        self.friday_week1_client6 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client6, width = 12)
        self.friday_week1_client6.grid(column = 8, row = 8, padx = 5, pady = 5)

        self.fridayweek1client7 = StringVar()
        self.friday_week1_client7 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client7, width = 12)
        self.friday_week1_client7.grid(column = 8, row = 9, padx = 5, pady = 5)

        self.fridayweek1client8 = StringVar()
        self.friday_week1_client8 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client8, width = 12)
        self.friday_week1_client8.grid(column = 8, row = 10, padx = 5, pady = 5)

        self.fridayweek1client9 = StringVar()
        self.friday_week1_client9 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client9, width = 12)
        self.friday_week1_client9.grid(column = 8, row = 11, padx = 5, pady = 5)

        self.fridayweek1client10 = StringVar()
        self.friday_week1_client10 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client10, width = 12)
        self.friday_week1_client10.grid(column = 8, row = 12, padx = 5, pady = 5)

        self.fridayweek1client11 = StringVar()
        self.friday_week1_client11 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client11, width = 12)
        self.friday_week1_client11.grid(column = 8, row = 13, padx = 5, pady = 5)

        self.fridayweek1client12 = StringVar()
        self.friday_week1_client12 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client12, width = 12)
        self.friday_week1_client12.grid(column = 8, row = 14, padx = 5, pady = 5)

        self.fridayweek1client13 = StringVar()
        self.friday_week1_client13 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client13, width = 12)
        self.friday_week1_client13.grid(column = 8, row = 15, padx = 5, pady = 5)

        self.fridayweek1client14 = StringVar()
        self.friday_week1_client14 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client14, width = 12)
        self.friday_week1_client14.grid(column = 8, row = 16, padx = 5, pady = 5)

        self.fridayweek1client15 = StringVar()
        self.friday_week1_client15 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client15, width = 12)
        self.friday_week1_client15.grid(column = 8, row = 17, padx = 5, pady = 5)

        self.fridayweek1client16 = StringVar()
        self.friday_week1_client16 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client16, width = 12)
        self.friday_week1_client16.grid(column = 8, row = 18, padx = 5, pady = 5)

        self.fridayweek1client17 = StringVar()
        self.friday_week1_client17 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client17, width = 12)
        self.friday_week1_client17.grid(column = 8, row = 19, padx = 5, pady = 5)

        self.fridayweek1client18 = StringVar()
        self.friday_week1_client18 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client18, width = 12)
        self.friday_week1_client18.grid(column = 8, row = 20, padx = 5, pady = 5)

        self.fridayweek1client19 = StringVar()
        self.friday_week1_client19= Entry(self.wrapper2frame, textvariable = self.fridayweek1client19, width = 12)
        self.friday_week1_client19.grid(column = 8, row = 21, padx = 5, pady = 5)

        self.fridayweek1client20 = StringVar()
        self.friday_week1_client20 = Entry(self.wrapper2frame, textvariable = self.fridayweek1client20, width = 12)
        self.friday_week1_client20.grid(column = 8, row = 22, padx = 5, pady = 5)

        #Client 1 field
        self.notes_client1 = StringVar()
        self.notes_client1_selection = Entry(self.wrapper2frame, textvariable = self.notes_client1, width = 12)
        self.notes_client1_selection.grid(column = 9, row = 3, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        self.notes_client2 = StringVar()
        self.notes_client2_selection = Entry(self.wrapper2frame, textvariable = self.notes_client2, width = 12)
        self.notes_client2_selection.grid(column = 9, row = 4, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        self.notes_client3 = StringVar()
        self.notes_client3_selection = Entry(self.wrapper2frame, textvariable = self.notes_client3, width = 12)
        self.notes_client3_selection.grid(column = 9, row = 5, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        self.notes_client4 = StringVar()
        self.notes_client4_selection = Entry(self.wrapper2frame, textvariable = self.notes_client4, width = 12)
        self.notes_client4_selection.grid(column = 9, row = 6, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        self.notes_client5 = StringVar()
        self.notes_client5_selection = Entry(self.wrapper2frame, textvariable = self.notes_client5, width = 12)
        self.notes_client5_selection.grid(column = 9, row = 7, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        self.notes_client6 = StringVar()
        self.notes_client6_selection = Entry(self.wrapper2frame, textvariable = self.notes_client6, width = 12)
        self.notes_client6_selection.grid(column = 9, row = 8, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        self.notes_client7 = StringVar()
        self.notes_client7_selection = Entry(self.wrapper2frame, textvariable = self.notes_client7, width = 12)
        self.notes_client7_selection.grid(column = 9, row = 9, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        self.notes_client8 = StringVar()
        self.notes_client8_selection = Entry(self.wrapper2frame, textvariable = self.notes_client8, width = 12)
        self.notes_client8_selection.grid(column = 9, row = 10, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        self.notes_client9 = StringVar()
        self.notes_client9_selection = Entry(self.wrapper2frame, textvariable = self.notes_client9, width = 12)
        self.notes_client9_selection.grid(column = 9, row = 11, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        self.notes_client10 = StringVar()
        self.notes_client10_selection = Entry(self.wrapper2frame, textvariable = self.notes_client10, width = 12)
        self.notes_client10_selection.grid(column = 9, row = 12, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        self.notes_client11 = StringVar()
        self.notes_client11_selection = Entry(self.wrapper2frame, textvariable = self.notes_client11, width = 12)
        self.notes_client11_selection.grid(column = 9, row = 13, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        self.notes_client12 = StringVar()
        self.notes_client12_selection = Entry(self.wrapper2frame, textvariable = self.notes_client12, width = 12)
        self.notes_client12_selection.grid(column = 9, row = 14, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        self.notes_client13 = StringVar()
        self.notes_client13_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client13_selection.grid(column = 9, row = 15, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        self.notes_client14 = StringVar()
        self.notes_client14_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client14_selection.grid(column = 9, row = 16, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        self.notes_client15 = StringVar()
        self.notes_client15_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client15_selection.grid(column = 9, row = 17, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        self.notes_client16 = StringVar()
        self.notes_client16_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client16_selection.grid(column = 9, row = 18, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        self.notes_client17 = StringVar()
        self.notes_client17_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client17_selection.grid(column = 9, row = 19, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        self.notes_client18 = StringVar()
        self.notes_client18_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client18_selection.grid(column = 9, row = 20, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        self.notes_client19 = StringVar()
        self.notes_client19_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client19_selection.grid(column = 9, row = 21, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        self.notes_client20 = StringVar()
        self.notes_client20_selection = Entry(self.wrapper2frame, textvariable = self.notes_client13, width = 12)
        self.notes_client20_selection.grid(column = 9, row = 22, columnspan = 1)

        self.notes_client1_notes = Button(self.wrapper2frame, image = self.notes_icon_resize)
        self.notes_client1_notes.grid(column = 10, row = 22, sticky = "we", padx = 5, pady = 5)

    def new_window(self, _class):
        global win2, Win3

        try:
            if _class == Win2:
                if win2.state() == "normal":
                    win2.focus()
        except:
            win2 = Toplevel(self.master)
            _class(win2)

        try:
            if _class == Win3:
                if win3.state() == "normal":
                    win3.focus()

        except:
            win3 = Toplevel(self.master)
            _class(win3)
    
    def close_window(self):
        self.master.destroy()

class Win2(MainPage):

    def show_widgets(self):
        self.master.title("Window 2")
        self.frame = Frame(self.master, bg = "red")
        self.quit_button = Button(self.frame, text = f"Quit window 3 from window 2", command = self.close_window)
        self.frame.pack()
        self.quit_button.pack()
        self.engagementcode_search("Open window 3 from window 2", Win3)
        self.frame.pack()

class Win3(Win2):
    def show_widgets(self):
        self.master.title("Window 3")
        self.frame = Frame(self.master, bg = "green")
        self.quit_button = Button(self.frame, text = f"Quit this window n. 3", command = self.close_window)
        self.label = Label(self.frame, text = "This is only in the third window.")
        self.label.pack()
        self.frame.pack()

root = Tk()
app = MainPage(root)
root.mainloop()