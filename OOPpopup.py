import os
import sys
import getpass
import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import *
import backend


LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

#global selected_code
engagementcode_client1_selection = selected_code.get()

def popupmsg():
    #popup = tk.Tk()
    #popup.wm_title("!")
    #label = ttk.Label(popup, text=msg, font=NORM_FONT)
    #label.pack(side="top", fill="x", pady=10)
    #B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    #B1.pack()

    screen = Tk()
    screen.wm_title("Time Entry Application")
    screen.geometry("200x200")
    #heading = Label(screen, text = "Add and Review Time Entries and Timesheets", bg = "grey", fg = "white")
    #heading.grid(column = 0, row = 0, columnspan = 16, rowspan = 2)

    def popupmsgcommands(selected_code):
        engagementcode_client1_selection.delete(0,END)
        engagementcode_client1_selection.insert(0,selected_code)
        return

    #def popupmsgcommands():
        #engagementcode_client1_selection = selected_code.get()
        #engagementcode_client1_selection.insert(END, selected_code.get())
        #os.environ["variable"] = selected_code.get()
        #screen.destroy()

    #Client field
    engagement_label = Label(screen, text = "Client", width = 40)
    engagement_label.pack(side="top", pady=5, padx=10)
    
    selected_client = StringVar()
    client1 = ttk.Combobox(screen, textvariable = selected_client, state = 'readonly')
    client1['values'] = backend.client_dropdown()
    client1.pack(side="top", padx=10)
    client1.get()

    #Engagement field
    engagement_label = Label(screen, text = "Engagement", width = 50)
    engagement_label.pack(side="top", pady=5, padx=10)
    
    selected_engagement = StringVar()
    engagement1 = ttk.Combobox(screen, textvariable = selected_engagement, state = 'readonly', postcommand = lambda: engagement1.configure(value = backend.engagement_dropdown(client1.get())))
    engagement1['values'] = backend.engagement_dropdown(client1.get())
    engagement1.pack(side="top", pady=5, padx=10)

    #Engagement Code field
    engagementcode_label = Label(screen, text = "Engagement Code", width = 40)
    engagementcode_label.pack(side="top", padx=10)
    
    selected_code = StringVar()
    code1 = ttk.Combobox(screen, textvariable = selected_code, state = 'readonly', postcommand = lambda: code1.configure(value = backend.engagementcode_dropdown(client1.get(), engagement1.get())))
    code1['values'] = backend.client_dropdown()
    code1.pack(side="top", pady=5, padx=10)
    code1.get()

    select_button = Button(screen, text = "Select", command = lambda: popupmsgcommands(selected_code))
    select_button.pack(side="top", pady=5, padx=10)
    screen.mainloop()

class MainPage(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Time Entry Application")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, ManagerPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    global engagementcode_client1_selection

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #Pay period field
        payperiod_label = Label(self, text = "Pay Period", width = 30)
        payperiod_label.grid(column = 0, row = 0, columnspan = 1, sticky = "w", padx = 5)

        payperiod_entry = StringVar()
        payperiod1 = ttk.Combobox(self, textvariable = payperiod_entry, state = 'readonly')
        payperiod1['values'] = backend.payperiod_dropdown()
        payperiod1.grid(column = 0, row = 1, columnspan = 1, sticky = "we", padx = 5)
        payperiod1.get()

        #Button to review pay period
        add_time_entry = Button(self, text = "Select", command = lambda: controller.show_frame(popupmsg()))
        #add_time_entry.pack()
        add_time_entry.grid(column = 3, row = 1, columnspan = 2, sticky = "we", padx = 5, pady = 5)

        #Tabs for Week 1 and Week 2
        tabControl = ttk.Notebook(self) 
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

        engagementcode_client1_search = Button(wrapper1frame, text = "Search", command = lambda: controller.show_frame(popupmsg()))
        engagementcode_client1_search.grid(column = 1, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        engagementcode_client2 = StringVar()
        engagementcode_client2_selection = Entry(wrapper1frame, textvariable = engagementcode_client2, width = 12)
        engagementcode_client2_selection.grid(column = 0, row = 4, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        engagementcode_client3 = StringVar()
        engagementcode_client3_selection = Entry(wrapper1frame, textvariable = engagementcode_client3, width = 12)
        engagementcode_client3_selection.grid(column = 0, row = 5, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        engagementcode_client4 = StringVar()
        engagementcode_client4_selection = Entry(wrapper1frame, textvariable = engagementcode_client4, width = 12)
        engagementcode_client4_selection.grid(column = 0, row = 6, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        engagementcode_client5 = StringVar()
        engagementcode_client5_selection = Entry(wrapper1frame, textvariable = engagementcode_client5, width = 12)
        engagementcode_client5_selection.grid(column = 0, row = 7, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        engagementcode_client6 = StringVar()
        engagementcode_client6_selection = Entry(wrapper1frame, textvariable = engagementcode_client6, width = 12)
        engagementcode_client6_selection.grid(column = 0, row = 8, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        engagementcode_client7 = StringVar()
        engagementcode_client7_selection = Entry(wrapper1frame, textvariable = engagementcode_client7, width = 12)
        engagementcode_client7_selection.grid(column = 0, row = 9, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        engagementcode_client8 = StringVar()
        engagementcode_client8_selection = Entry(wrapper1frame, textvariable = engagementcode_client8, width = 12)
        engagementcode_client8_selection.grid(column = 0, row = 10, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        engagementcode_client9 = StringVar()
        engagementcode_client9_selection = Entry(wrapper1frame, textvariable = engagementcode_client9, width = 12)
        engagementcode_client9_selection.grid(column = 0, row = 11, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        engagementcode_client10 = StringVar()
        engagementcode_client10_selection = Entry(wrapper1frame, textvariable = engagementcode_client10, width = 12)
        engagementcode_client10_selection.grid(column = 0, row = 12, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        engagementcode_client11 = StringVar()
        engagementcode_client11_selection = Entry(wrapper1frame, textvariable = engagementcode_client11, width = 12)
        engagementcode_client11_selection.grid(column = 0, row = 13, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        engagementcode_client12 = StringVar()
        engagementcode_client12_selection = Entry(wrapper1frame, textvariable = engagementcode_client12, width = 12)
        engagementcode_client12_selection.grid(column = 0, row = 14, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        engagementcode_client13 = StringVar()
        engagementcode_client13_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client13_selection.grid(column = 0, row = 15, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        engagementcode_client14 = StringVar()
        engagementcode_client14_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client14_selection.grid(column = 0, row = 16, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        engagementcode_client15 = StringVar()
        engagementcode_client15_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client15_selection.grid(column = 0, row = 17, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        engagementcode_client16 = StringVar()
        engagementcode_client16_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client16_selection.grid(column = 0, row = 18, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        engagementcode_client17 = StringVar()
        engagementcode_client17_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client17_selection.grid(column = 0, row = 19, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        engagementcode_client18 = StringVar()
        engagementcode_client18_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client18_selection.grid(column = 0, row = 20, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        engagementcode_client19 = StringVar()
        engagementcode_client19_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client19_selection.grid(column = 0, row = 21, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        engagementcode_client20 = StringVar()
        engagementcode_client20_selection = Entry(wrapper1frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client20_selection.grid(column = 0, row = 22, columnspan = 1)

        engagementcode_client1_search = Button(wrapper1frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 22, sticky = "we", padx = 5, pady = 5)

        #Weekday hours field example
        saturdayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = saturdayweek1, width = 12)
        week1_label.grid(column = 2, row = 2, padx = 5, pady = 5)

        saturdayweek1client1 = StringVar()
        saturday_week1_client1 = Entry(wrapper1frame, textvariable = saturdayweek1client1, width = 12)
        saturday_week1_client1.grid(column = 2, row = 3, padx = 5, pady = 5)

        saturdayweek1client2 = StringVar()
        saturday_week1_client2 = Entry(wrapper1frame, textvariable = saturdayweek1client2, width = 12)
        saturday_week1_client2.grid(column = 2, row = 4, padx = 5, pady = 5)

        saturdayweek1client3 = StringVar()
        saturday_week1_client3 = Entry(wrapper1frame, textvariable = saturdayweek1client3, width = 12)
        saturday_week1_client3.grid(column = 2, row = 5, padx = 5, pady = 5)

        saturdayweek1client4 = StringVar()
        saturday_week1_client4 = Entry(wrapper1frame, textvariable = saturdayweek1client4, width = 12)
        saturday_week1_client4.grid(column = 2, row = 6, padx = 5, pady = 5)

        saturdayweek1client5 = StringVar()
        saturday_week1_client5 = Entry(wrapper1frame, textvariable = saturdayweek1client5, width = 12)
        saturday_week1_client5.grid(column = 2, row = 7, padx = 5, pady = 5)

        saturdayweek1client6 = StringVar()
        saturday_week1_client6 = Entry(wrapper1frame, textvariable = saturdayweek1client6, width = 12)
        saturday_week1_client6.grid(column = 2, row = 8, padx = 5, pady = 5)

        saturdayweek1client7 = StringVar()
        saturday_week1_client7 = Entry(wrapper1frame, textvariable = saturdayweek1client7, width = 12)
        saturday_week1_client7.grid(column = 2, row = 9, padx = 5, pady = 5)

        saturdayweek1client8 = StringVar()
        saturday_week1_client8 = Entry(wrapper1frame, textvariable = saturdayweek1client8, width = 12)
        saturday_week1_client8.grid(column = 2, row = 10, padx = 5, pady = 5)

        saturdayweek1client9 = StringVar()
        saturday_week1_client9 = Entry(wrapper1frame, textvariable = saturdayweek1client9, width = 12)
        saturday_week1_client9.grid(column = 2, row = 11, padx = 5, pady = 5)

        saturdayweek1client10 = StringVar()
        saturday_week1_client10 = Entry(wrapper1frame, textvariable = saturdayweek1client10, width = 12)
        saturday_week1_client10.grid(column = 2, row = 12, padx = 5, pady = 5)

        saturdayweek1client11 = StringVar()
        saturday_week1_client11 = Entry(wrapper1frame, textvariable = saturdayweek1client11, width = 12)
        saturday_week1_client11.grid(column = 2, row = 13, padx = 5, pady = 5)

        saturdayweek1client12 = StringVar()
        saturday_week1_client12 = Entry(wrapper1frame, textvariable = saturdayweek1client12, width = 12)
        saturday_week1_client12.grid(column = 2, row = 14, padx = 5, pady = 5)

        saturdayweek1client13 = StringVar()
        saturday_week1_client13 = Entry(wrapper1frame, textvariable = saturdayweek1client13, width = 12)
        saturday_week1_client13.grid(column = 2, row = 15, padx = 5, pady = 5)

        saturdayweek1client14 = StringVar()
        saturday_week1_client14 = Entry(wrapper1frame, textvariable = saturdayweek1client14, width = 12)
        saturday_week1_client14.grid(column = 2, row = 16, padx = 5, pady = 5)

        saturdayweek1client15 = StringVar()
        saturday_week1_client15 = Entry(wrapper1frame, textvariable = saturdayweek1client15, width = 12)
        saturday_week1_client15.grid(column = 2, row = 17, padx = 5, pady = 5)

        saturdayweek1client16 = StringVar()
        saturday_week1_client16 = Entry(wrapper1frame, textvariable = saturdayweek1client16, width = 12)
        saturday_week1_client16.grid(column = 2, row = 18, padx = 5, pady = 5)

        saturdayweek1client17 = StringVar()
        saturday_week1_client17 = Entry(wrapper1frame, textvariable = saturdayweek1client17, width = 12)
        saturday_week1_client17.grid(column = 2, row = 19, padx = 5, pady = 5)

        saturdayweek1client18 = StringVar()
        saturday_week1_client18 = Entry(wrapper1frame, textvariable = saturdayweek1client18, width = 12)
        saturday_week1_client18.grid(column = 2, row = 20, padx = 5, pady = 5)

        saturdayweek1client19 = StringVar()
        saturday_week1_client19= Entry(wrapper1frame, textvariable = saturdayweek1client19, width = 12)
        saturday_week1_client19.grid(column = 2, row = 21, padx = 5, pady = 5)

        saturdayweek1client20 = StringVar()
        saturday_week1_client20 = Entry(wrapper1frame, textvariable = saturdayweek1client20, width = 12)
        saturday_week1_client20.grid(column = 2, row = 22, padx = 5, pady = 5)

        sundayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = sundayweek1, width = 12)
        week1_label.grid(column = 3, row = 2, padx = 5, pady = 5)

        sundayweek1client1 = StringVar()
        sunday_week1_client1 = Entry(wrapper1frame, textvariable = sundayweek1client1, width = 12)
        sunday_week1_client1.grid(column = 3, row = 3, padx = 5, pady = 5)

        sundayweek1client2 = StringVar()
        sunday_week1_client2 = Entry(wrapper1frame, textvariable = sundayweek1client2, width = 12)
        sunday_week1_client2.grid(column = 3, row = 4, padx = 5, pady = 5)

        sundayweek1client3 = StringVar()
        sunday_week1_client3 = Entry(wrapper1frame, textvariable = sundayweek1client3, width = 12)
        sunday_week1_client3.grid(column = 3, row = 5, padx = 5, pady = 5)

        sundayweek1client4 = StringVar()
        sunday_week1_client4 = Entry(wrapper1frame, textvariable = sundayweek1client4, width = 12)
        sunday_week1_client4.grid(column = 3, row = 6, padx = 5, pady = 5)

        sundayweek1client5 = StringVar()
        sunday_week1_client5 = Entry(wrapper1frame, textvariable = sundayweek1client5, width = 12)
        sunday_week1_client5.grid(column = 3, row = 7, padx = 5, pady = 5)

        sundayweek1client6 = StringVar()
        sunday_week1_client6 = Entry(wrapper1frame, textvariable = sundayweek1client6, width = 12)
        sunday_week1_client6.grid(column = 3, row = 8, padx = 5, pady = 5)

        sundayweek1client7 = StringVar()
        sunday_week1_client7 = Entry(wrapper1frame, textvariable = sundayweek1client7, width = 12)
        sunday_week1_client7.grid(column = 3, row = 9, padx = 5, pady = 5)

        sundayweek1client8 = StringVar()
        sunday_week1_client8 = Entry(wrapper1frame, textvariable = sundayweek1client8, width = 12)
        sunday_week1_client8.grid(column = 3, row = 10, padx = 5, pady = 5)

        sundayweek1client9 = StringVar()
        sunday_week1_client9 = Entry(wrapper1frame, textvariable = sundayweek1client9, width = 12)
        sunday_week1_client9.grid(column = 3, row = 11, padx = 5, pady = 5)

        sundayweek1client10 = StringVar()
        sunday_week1_client10 = Entry(wrapper1frame, textvariable = sundayweek1client10, width = 12)
        sunday_week1_client10.grid(column = 3, row = 12, padx = 5, pady = 5)

        sundayweek1client11 = StringVar()
        sunday_week1_client11 = Entry(wrapper1frame, textvariable = sundayweek1client11, width = 12)
        sunday_week1_client11.grid(column = 3, row = 13, padx = 5, pady = 5)

        sundayweek1client12 = StringVar()
        sunday_week1_client12 = Entry(wrapper1frame, textvariable = sundayweek1client12, width = 12)
        sunday_week1_client12.grid(column = 3, row = 14, padx = 5, pady = 5)

        sundayweek1client13 = StringVar()
        sunday_week1_client13 = Entry(wrapper1frame, textvariable = sundayweek1client13, width = 12)
        sunday_week1_client13.grid(column = 3, row = 15, padx = 5, pady = 5)

        sundayweek1client14 = StringVar()
        sunday_week1_client14 = Entry(wrapper1frame, textvariable = sundayweek1client14, width = 12)
        sunday_week1_client14.grid(column = 3, row = 16, padx = 5, pady = 5)

        sundayweek1client15 = StringVar()
        sunday_week1_client15 = Entry(wrapper1frame, textvariable = sundayweek1client15, width = 12)
        sunday_week1_client15.grid(column = 3, row = 17, padx = 5, pady = 5)

        sundayweek1client16 = StringVar()
        sunday_week1_client16 = Entry(wrapper1frame, textvariable = sundayweek1client16, width = 12)
        sunday_week1_client16.grid(column = 3, row = 18, padx = 5, pady = 5)

        sundayweek1client17 = StringVar()
        sunday_week1_client17 = Entry(wrapper1frame, textvariable = sundayweek1client17, width = 12)
        sunday_week1_client17.grid(column = 3, row = 19, padx = 5, pady = 5)

        sundayweek1client18 = StringVar()
        sunday_week1_client18 = Entry(wrapper1frame, textvariable = sundayweek1client18, width = 12)
        sunday_week1_client18.grid(column = 3, row = 20, padx = 5, pady = 5)

        sundayweek1client19 = StringVar()
        sunday_week1_client19= Entry(wrapper1frame, textvariable = sundayweek1client19, width = 12)
        sunday_week1_client19.grid(column = 3, row = 21, padx = 5, pady = 5)

        sundayweek1client20 = StringVar()
        sunday_week1_client20 = Entry(wrapper1frame, textvariable = sundayweek1client20, width = 12)
        sunday_week1_client20.grid(column = 3, row = 22, padx = 5, pady = 5)

        mondayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = mondayweek1, width = 12)
        week1_label.grid(column = 4, row = 2, padx = 5, pady = 5)

        mondayweek1client1 = StringVar()
        monday_week1_client1 = Entry(wrapper1frame, textvariable = mondayweek1client1, width = 12)
        monday_week1_client1.grid(column = 4, row = 3, padx = 5, pady = 5)

        mondayweek1client2 = StringVar()
        monday_week1_client2 = Entry(wrapper1frame, textvariable = mondayweek1client2, width = 12)
        monday_week1_client2.grid(column = 4, row = 4, padx = 5, pady = 5)

        mondayweek1client3 = StringVar()
        monday_week1_client3 = Entry(wrapper1frame, textvariable = mondayweek1client3, width = 12)
        monday_week1_client3.grid(column = 4, row = 5, padx = 5, pady = 5)

        mondayweek1client4 = StringVar()
        monday_week1_client4 = Entry(wrapper1frame, textvariable = mondayweek1client4, width = 12)
        monday_week1_client4.grid(column = 4, row = 6, padx = 5, pady = 5)

        mondayweek1client5 = StringVar()
        monday_week1_client5 = Entry(wrapper1frame, textvariable = mondayweek1client5, width = 12)
        monday_week1_client5.grid(column = 4, row = 7, padx = 5, pady = 5)

        mondayweek1client6 = StringVar()
        monday_week1_client6 = Entry(wrapper1frame, textvariable = mondayweek1client6, width = 12)
        monday_week1_client6.grid(column = 4, row = 8, padx = 5, pady = 5)

        mondayweek1client7 = StringVar()
        monday_week1_client7 = Entry(wrapper1frame, textvariable = mondayweek1client7, width = 12)
        monday_week1_client7.grid(column = 4, row = 9, padx = 5, pady = 5)

        mondayweek1client8 = StringVar()
        monday_week1_client8 = Entry(wrapper1frame, textvariable = mondayweek1client8, width = 12)
        monday_week1_client8.grid(column = 4, row = 10, padx = 5, pady = 5)

        mondayweek1client9 = StringVar()
        monday_week1_client9 = Entry(wrapper1frame, textvariable = mondayweek1client9, width = 12)
        monday_week1_client9.grid(column = 4, row = 11, padx = 5, pady = 5)

        mondayweek1client10 = StringVar()
        monday_week1_client10 = Entry(wrapper1frame, textvariable = mondayweek1client10, width = 12)
        monday_week1_client10.grid(column = 4, row = 12, padx = 5, pady = 5)

        mondayweek1client11 = StringVar()
        monday_week1_client11 = Entry(wrapper1frame, textvariable = mondayweek1client11, width = 12)
        monday_week1_client11.grid(column = 4, row = 13, padx = 5, pady = 5)

        mondayweek1client12 = StringVar()
        monday_week1_client12 = Entry(wrapper1frame, textvariable = mondayweek1client12, width = 12)
        monday_week1_client12.grid(column = 4, row = 14, padx = 5, pady = 5)

        mondayweek1client13 = StringVar()
        monday_week1_client13 = Entry(wrapper1frame, textvariable = mondayweek1client13, width = 12)
        monday_week1_client13.grid(column = 4, row = 15, padx = 5, pady = 5)

        mondayweek1client14 = StringVar()
        monday_week1_client14 = Entry(wrapper1frame, textvariable = mondayweek1client14, width = 12)
        monday_week1_client14.grid(column = 4, row = 16, padx = 5, pady = 5)

        mondayweek1client15 = StringVar()
        monday_week1_client15 = Entry(wrapper1frame, textvariable = mondayweek1client15, width = 12)
        monday_week1_client15.grid(column = 4, row = 17, padx = 5, pady = 5)

        mondayweek1client16 = StringVar()
        monday_week1_client16 = Entry(wrapper1frame, textvariable = mondayweek1client16, width = 12)
        monday_week1_client16.grid(column = 4, row = 18, padx = 5, pady = 5)

        mondayweek1client17 = StringVar()
        monday_week1_client17 = Entry(wrapper1frame, textvariable = mondayweek1client17, width = 12)
        monday_week1_client17.grid(column = 4, row = 19, padx = 5, pady = 5)

        mondayweek1client18 = StringVar()
        monday_week1_client18 = Entry(wrapper1frame, textvariable = mondayweek1client18, width = 12)
        monday_week1_client18.grid(column = 4, row = 20, padx = 5, pady = 5)

        mondayweek1client19 = StringVar()
        monday_week1_client19= Entry(wrapper1frame, textvariable = mondayweek1client19, width = 12)
        monday_week1_client19.grid(column = 4, row = 21, padx = 5, pady = 5)

        mondayweek1client20 = StringVar()
        monday_week1_client20 = Entry(wrapper1frame, textvariable = mondayweek1client20, width = 12)
        monday_week1_client20.grid(column = 4, row = 22, padx = 5, pady = 5)

        tuesdayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = tuesdayweek1, width = 12)
        week1_label.grid(column = 5, row = 2, padx = 5, pady = 5)

        tuesdayweek1client1 = StringVar()
        tuesday_week1_client1 = Entry(wrapper1frame, textvariable = tuesdayweek1client1, width = 12)
        tuesday_week1_client1.grid(column = 5, row = 3, padx = 5, pady = 5)

        tuesdayweek1client2 = StringVar()
        tuesday_week1_client2 = Entry(wrapper1frame, textvariable = tuesdayweek1client2, width = 12)
        tuesday_week1_client2.grid(column = 5, row = 4, padx = 5, pady = 5)

        tuesdayweek1client3 = StringVar()
        tuesday_week1_client3 = Entry(wrapper1frame, textvariable = tuesdayweek1client3, width = 12)
        tuesday_week1_client3.grid(column = 5, row = 5, padx = 5, pady = 5)

        tuesdayweek1client4 = StringVar()
        tuesday_week1_client4 = Entry(wrapper1frame, textvariable = tuesdayweek1client4, width = 12)
        tuesday_week1_client4.grid(column = 5, row = 6, padx = 5, pady = 5)

        tuesdayweek1client5 = StringVar()
        tuesday_week1_client5 = Entry(wrapper1frame, textvariable = tuesdayweek1client5, width = 12)
        tuesday_week1_client5.grid(column = 5, row = 7, padx = 5, pady = 5)

        tuesdayweek1client6 = StringVar()
        tuesday_week1_client6 = Entry(wrapper1frame, textvariable = tuesdayweek1client6, width = 12)
        tuesday_week1_client6.grid(column = 5, row = 8, padx = 5, pady = 5)

        tuesdayweek1client7 = StringVar()
        tuesday_week1_client7 = Entry(wrapper1frame, textvariable = tuesdayweek1client7, width = 12)
        tuesday_week1_client7.grid(column = 5, row = 9, padx = 5, pady = 5)

        tuesdayweek1client8 = StringVar()
        tuesday_week1_client8 = Entry(wrapper1frame, textvariable = tuesdayweek1client8, width = 12)
        tuesday_week1_client8.grid(column = 5, row = 10, padx = 5, pady = 5)

        tuesdayweek1client9 = StringVar()
        tuesday_week1_client9 = Entry(wrapper1frame, textvariable = tuesdayweek1client9, width = 12)
        tuesday_week1_client9.grid(column = 5, row = 11, padx = 5, pady = 5)

        tuesdayweek1client10 = StringVar()
        tuesday_week1_client10 = Entry(wrapper1frame, textvariable = tuesdayweek1client10, width = 12)
        tuesday_week1_client10.grid(column = 5, row = 12, padx = 5, pady = 5)

        tuesdayweek1client11 = StringVar()
        tuesday_week1_client11 = Entry(wrapper1frame, textvariable = tuesdayweek1client11, width = 12)
        tuesday_week1_client11.grid(column = 5, row = 13, padx = 5, pady = 5)

        tuesdayweek1client12 = StringVar()
        tuesday_week1_client12 = Entry(wrapper1frame, textvariable = tuesdayweek1client12, width = 12)
        tuesday_week1_client12.grid(column = 5, row = 14, padx = 5, pady = 5)

        tuesdayweek1client13 = StringVar()
        tuesday_week1_client13 = Entry(wrapper1frame, textvariable = tuesdayweek1client13, width = 12)
        tuesday_week1_client13.grid(column = 5, row = 15, padx = 5, pady = 5)

        tuesdayweek1client14 = StringVar()
        tuesday_week1_client14 = Entry(wrapper1frame, textvariable = tuesdayweek1client14, width = 12)
        tuesday_week1_client14.grid(column = 5, row = 16, padx = 5, pady = 5)

        tuesdayweek1client15 = StringVar()
        tuesday_week1_client15 = Entry(wrapper1frame, textvariable = tuesdayweek1client15, width = 12)
        tuesday_week1_client15.grid(column = 5, row = 17, padx = 5, pady = 5)

        tuesdayweek1client16 = StringVar()
        tuesday_week1_client16 = Entry(wrapper1frame, textvariable = tuesdayweek1client16, width = 12)
        tuesday_week1_client16.grid(column = 5, row = 18, padx = 5, pady = 5)

        tuesdayweek1client17 = StringVar()
        tuesday_week1_client17 = Entry(wrapper1frame, textvariable = tuesdayweek1client17, width = 12)
        tuesday_week1_client17.grid(column = 5, row = 19, padx = 5, pady = 5)

        tuesdayweek1client18 = StringVar()
        tuesday_week1_client18 = Entry(wrapper1frame, textvariable = tuesdayweek1client18, width = 12)
        tuesday_week1_client18.grid(column = 5, row = 20, padx = 5, pady = 5)

        tuesdayweek1client19 = StringVar()
        tuesday_week1_client19= Entry(wrapper1frame, textvariable = tuesdayweek1client19, width = 12)
        tuesday_week1_client19.grid(column = 5, row = 21, padx = 5, pady = 5)

        tuesdayweek1client20 = StringVar()
        tuesday_week1_client20 = Entry(wrapper1frame, textvariable = tuesdayweek1client20, width = 12)
        tuesday_week1_client20.grid(column = 5, row = 22, padx = 5, pady = 5)

        wednesdayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = wednesdayweek1, width = 12)
        week1_label.grid(column = 6, row = 2, padx = 5, pady = 5)

        wednesdayweek1client1 = StringVar()
        wednesday_week1_client1 = Entry(wrapper1frame, textvariable = wednesdayweek1client1, width = 12)
        wednesday_week1_client1.grid(column = 6, row = 3, padx = 5, pady = 5)

        wednesdayweek1client2 = StringVar()
        wednesday_week1_client2 = Entry(wrapper1frame, textvariable = wednesdayweek1client2, width = 12)
        wednesday_week1_client2.grid(column = 6, row = 4, padx = 5, pady = 5)

        wednesdayweek1client3 = StringVar()
        wednesday_week1_client3 = Entry(wrapper1frame, textvariable = wednesdayweek1client3, width = 12)
        wednesday_week1_client3.grid(column = 6, row = 5, padx = 5, pady = 5)

        wednesdayweek1client4 = StringVar()
        wednesday_week1_client4 = Entry(wrapper1frame, textvariable = wednesdayweek1client4, width = 12)
        wednesday_week1_client4.grid(column = 6, row = 6, padx = 5, pady = 5)

        wednesdayweek1client5 = StringVar()
        wednesday_week1_client5 = Entry(wrapper1frame, textvariable = wednesdayweek1client5, width = 12)
        wednesday_week1_client5.grid(column = 6, row = 7, padx = 5, pady = 5)

        wednesdayweek1client6 = StringVar()
        wednesday_week1_client6 = Entry(wrapper1frame, textvariable = wednesdayweek1client6, width = 12)
        wednesday_week1_client6.grid(column = 6, row = 8, padx = 5, pady = 5)

        wednesdayweek1client7 = StringVar()
        wednesday_week1_client7 = Entry(wrapper1frame, textvariable = wednesdayweek1client7, width = 12)
        wednesday_week1_client7.grid(column = 6, row = 9, padx = 5, pady = 5)

        wednesdayweek1client8 = StringVar()
        wednesday_week1_client8 = Entry(wrapper1frame, textvariable = wednesdayweek1client8, width = 12)
        wednesday_week1_client8.grid(column = 6, row = 10, padx = 5, pady = 5)

        wednesdayweek1client9 = StringVar()
        wednesday_week1_client9 = Entry(wrapper1frame, textvariable = wednesdayweek1client9, width = 12)
        wednesday_week1_client9.grid(column = 6, row = 11, padx = 5, pady = 5)

        wednesdayweek1client10 = StringVar()
        wednesday_week1_client10 = Entry(wrapper1frame, textvariable = wednesdayweek1client10, width = 12)
        wednesday_week1_client10.grid(column = 6, row = 12, padx = 5, pady = 5)

        wednesdayweek1client11 = StringVar()
        wednesday_week1_client11 = Entry(wrapper1frame, textvariable = wednesdayweek1client11, width = 12)
        wednesday_week1_client11.grid(column = 6, row = 13, padx = 5, pady = 5)

        wednesdayweek1client12 = StringVar()
        wednesday_week1_client12 = Entry(wrapper1frame, textvariable = wednesdayweek1client12, width = 12)
        wednesday_week1_client12.grid(column = 6, row = 14, padx = 5, pady = 5)

        wednesdayweek1client13 = StringVar()
        wednesday_week1_client13 = Entry(wrapper1frame, textvariable = wednesdayweek1client13, width = 12)
        wednesday_week1_client13.grid(column = 6, row = 15, padx = 5, pady = 5)

        wednesdayweek1client14 = StringVar()
        wednesday_week1_client14 = Entry(wrapper1frame, textvariable = wednesdayweek1client14, width = 12)
        wednesday_week1_client14.grid(column = 6, row = 16, padx = 5, pady = 5)

        wednesdayweek1client15 = StringVar()
        wednesday_week1_client15 = Entry(wrapper1frame, textvariable = wednesdayweek1client15, width = 12)
        wednesday_week1_client15.grid(column = 6, row = 17, padx = 5, pady = 5)

        wednesdayweek1client16 = StringVar()
        wednesday_week1_client16 = Entry(wrapper1frame, textvariable = wednesdayweek1client16, width = 12)
        wednesday_week1_client16.grid(column = 6, row = 18, padx = 5, pady = 5)

        wednesdayweek1client17 = StringVar()
        wednesday_week1_client17 = Entry(wrapper1frame, textvariable = wednesdayweek1client17, width = 12)
        wednesday_week1_client17.grid(column = 6, row = 19, padx = 5, pady = 5)

        wednesdayweek1client18 = StringVar()
        wednesday_week1_client18 = Entry(wrapper1frame, textvariable = wednesdayweek1client18, width = 12)
        wednesday_week1_client18.grid(column = 6, row = 20, padx = 5, pady = 5)

        wednesdayweek1client19 = StringVar()
        wednesday_week1_client19= Entry(wrapper1frame, textvariable = wednesdayweek1client19, width = 12)
        wednesday_week1_client19.grid(column = 6, row = 21, padx = 5, pady = 5)

        wednesdayweek1client20 = StringVar()
        wednesday_week1_client20 = Entry(wrapper1frame, textvariable = wednesdayweek1client20, width = 12)
        wednesday_week1_client20.grid(column = 6, row = 22, padx = 5, pady = 5)

        thursdayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = thursdayweek1, width = 12)
        week1_label.grid(column = 7, row = 2, padx = 5, pady = 5)

        thursdayweek1client1 = StringVar()
        thursday_week1_client1 = Entry(wrapper1frame, textvariable = thursdayweek1client1, width = 12)
        thursday_week1_client1.grid(column = 7, row = 3, padx = 5, pady = 5)

        thursdayweek1client2 = StringVar()
        thursday_week1_client2 = Entry(wrapper1frame, textvariable = thursdayweek1client2, width = 12)
        thursday_week1_client2.grid(column = 7, row = 4, padx = 5, pady = 5)

        thursdayweek1client3 = StringVar()
        thursday_week1_client3 = Entry(wrapper1frame, textvariable = thursdayweek1client3, width = 12)
        thursday_week1_client3.grid(column = 7, row = 5, padx = 5, pady = 5)

        thursdayweek1client4 = StringVar()
        thursday_week1_client4 = Entry(wrapper1frame, textvariable = thursdayweek1client4, width = 12)
        thursday_week1_client4.grid(column = 7, row = 6, padx = 5, pady = 5)

        thursdayweek1client5 = StringVar()
        thursday_week1_client5 = Entry(wrapper1frame, textvariable = thursdayweek1client5, width = 12)
        thursday_week1_client5.grid(column = 7, row = 7, padx = 5, pady = 5)

        thursdayweek1client6 = StringVar()
        thursday_week1_client6 = Entry(wrapper1frame, textvariable = thursdayweek1client6, width = 12)
        thursday_week1_client6.grid(column = 7, row = 8, padx = 5, pady = 5)

        thursdayweek1client7 = StringVar()
        thursday_week1_client7 = Entry(wrapper1frame, textvariable = thursdayweek1client7, width = 12)
        thursday_week1_client7.grid(column = 7, row = 9, padx = 5, pady = 5)

        thursdayweek1client8 = StringVar()
        thursday_week1_client8 = Entry(wrapper1frame, textvariable = thursdayweek1client8, width = 12)
        thursday_week1_client8.grid(column = 7, row = 10, padx = 5, pady = 5)

        thursdayweek1client9 = StringVar()
        thursday_week1_client9 = Entry(wrapper1frame, textvariable = thursdayweek1client9, width = 12)
        thursday_week1_client9.grid(column = 7, row = 11, padx = 5, pady = 5)

        thursdayweek1client10 = StringVar()
        thursday_week1_client10 = Entry(wrapper1frame, textvariable = thursdayweek1client10, width = 12)
        thursday_week1_client10.grid(column = 7, row = 12, padx = 5, pady = 5)

        thursdayweek1client11 = StringVar()
        thursday_week1_client11 = Entry(wrapper1frame, textvariable = thursdayweek1client11, width = 12)
        thursday_week1_client11.grid(column = 7, row = 13, padx = 5, pady = 5)

        thursdayweek1client12 = StringVar()
        thursday_week1_client12 = Entry(wrapper1frame, textvariable = thursdayweek1client12, width = 12)
        thursday_week1_client12.grid(column = 7, row = 14, padx = 5, pady = 5)

        thursdayweek1client13 = StringVar()
        thursday_week1_client13 = Entry(wrapper1frame, textvariable = thursdayweek1client13, width = 12)
        thursday_week1_client13.grid(column = 7, row = 15, padx = 5, pady = 5)

        thursdayweek1client14 = StringVar()
        thursday_week1_client14 = Entry(wrapper1frame, textvariable = thursdayweek1client14, width = 12)
        thursday_week1_client14.grid(column = 7, row = 16, padx = 5, pady = 5)

        thursdayweek1client15 = StringVar()
        thursday_week1_client15 = Entry(wrapper1frame, textvariable = thursdayweek1client15, width = 12)
        thursday_week1_client15.grid(column = 7, row = 17, padx = 5, pady = 5)

        thursdayweek1client16 = StringVar()
        thursday_week1_client16 = Entry(wrapper1frame, textvariable = thursdayweek1client16, width = 12)
        thursday_week1_client16.grid(column = 7, row = 18, padx = 5, pady = 5)

        thursdayweek1client17 = StringVar()
        thursday_week1_client17 = Entry(wrapper1frame, textvariable = thursdayweek1client17, width = 12)
        thursday_week1_client17.grid(column = 7, row = 19, padx = 5, pady = 5)

        thursdayweek1client18 = StringVar()
        thursday_week1_client18 = Entry(wrapper1frame, textvariable = thursdayweek1client18, width = 12)
        thursday_week1_client18.grid(column = 7, row = 20, padx = 5, pady = 5)

        thursdayweek1client19 = StringVar()
        thursday_week1_client19= Entry(wrapper1frame, textvariable = thursdayweek1client19, width = 12)
        thursday_week1_client19.grid(column = 7, row = 21, padx = 5, pady = 5)

        thursdayweek1client20 = StringVar()
        thursday_week1_client20 = Entry(wrapper1frame, textvariable = thursdayweek1client20, width = 12)
        thursday_week1_client20.grid(column = 7, row = 22, padx = 5, pady = 5)

        fridayweek1 = StringVar()
        week1_label = Entry(wrapper1frame, textvariable = fridayweek1, width = 12)
        week1_label.grid(column = 8, row = 2, padx = 5, pady = 5)

        fridayweek1client1 = StringVar()
        friday_week1_client1 = Entry(wrapper1frame, textvariable = fridayweek1client1, width = 12)
        friday_week1_client1.grid(column = 8, row = 3, padx = 5, pady = 5)

        fridayweek1client2 = StringVar()
        friday_week1_client2 = Entry(wrapper1frame, textvariable = fridayweek1client2, width = 12)
        friday_week1_client2.grid(column = 8, row = 4, padx = 5, pady = 5)

        fridayweek1client3 = StringVar()
        friday_week1_client3 = Entry(wrapper1frame, textvariable = fridayweek1client3, width = 12)
        friday_week1_client3.grid(column = 8, row = 5, padx = 5, pady = 5)

        fridayweek1client4 = StringVar()
        friday_week1_client4 = Entry(wrapper1frame, textvariable = fridayweek1client4, width = 12)
        friday_week1_client4.grid(column = 8, row = 6, padx = 5, pady = 5)

        fridayweek1client5 = StringVar()
        friday_week1_client5 = Entry(wrapper1frame, textvariable = fridayweek1client5, width = 12)
        friday_week1_client5.grid(column = 8, row = 7, padx = 5, pady = 5)

        fridayweek1client6 = StringVar()
        friday_week1_client6 = Entry(wrapper1frame, textvariable = fridayweek1client6, width = 12)
        friday_week1_client6.grid(column = 8, row = 8, padx = 5, pady = 5)

        fridayweek1client7 = StringVar()
        friday_week1_client7 = Entry(wrapper1frame, textvariable = fridayweek1client7, width = 12)
        friday_week1_client7.grid(column = 8, row = 9, padx = 5, pady = 5)

        fridayweek1client8 = StringVar()
        friday_week1_client8 = Entry(wrapper1frame, textvariable = fridayweek1client8, width = 12)
        friday_week1_client8.grid(column = 8, row = 10, padx = 5, pady = 5)

        fridayweek1client9 = StringVar()
        friday_week1_client9 = Entry(wrapper1frame, textvariable = fridayweek1client9, width = 12)
        friday_week1_client9.grid(column = 8, row = 11, padx = 5, pady = 5)

        fridayweek1client10 = StringVar()
        friday_week1_client10 = Entry(wrapper1frame, textvariable = fridayweek1client10, width = 12)
        friday_week1_client10.grid(column = 8, row = 12, padx = 5, pady = 5)

        fridayweek1client11 = StringVar()
        friday_week1_client11 = Entry(wrapper1frame, textvariable = fridayweek1client11, width = 12)
        friday_week1_client11.grid(column = 8, row = 13, padx = 5, pady = 5)

        fridayweek1client12 = StringVar()
        friday_week1_client12 = Entry(wrapper1frame, textvariable = fridayweek1client12, width = 12)
        friday_week1_client12.grid(column = 8, row = 14, padx = 5, pady = 5)

        fridayweek1client13 = StringVar()
        friday_week1_client13 = Entry(wrapper1frame, textvariable = fridayweek1client13, width = 12)
        friday_week1_client13.grid(column = 8, row = 15, padx = 5, pady = 5)

        fridayweek1client14 = StringVar()
        friday_week1_client14 = Entry(wrapper1frame, textvariable = fridayweek1client14, width = 12)
        friday_week1_client14.grid(column = 8, row = 16, padx = 5, pady = 5)

        fridayweek1client15 = StringVar()
        friday_week1_client15 = Entry(wrapper1frame, textvariable = fridayweek1client15, width = 12)
        friday_week1_client15.grid(column = 8, row = 17, padx = 5, pady = 5)

        fridayweek1client16 = StringVar()
        friday_week1_client16 = Entry(wrapper1frame, textvariable = fridayweek1client16, width = 12)
        friday_week1_client16.grid(column = 8, row = 18, padx = 5, pady = 5)

        fridayweek1client17 = StringVar()
        friday_week1_client17 = Entry(wrapper1frame, textvariable = fridayweek1client17, width = 12)
        friday_week1_client17.grid(column = 8, row = 19, padx = 5, pady = 5)

        fridayweek1client18 = StringVar()
        friday_week1_client18 = Entry(wrapper1frame, textvariable = fridayweek1client18, width = 12)
        friday_week1_client18.grid(column = 8, row = 20, padx = 5, pady = 5)

        fridayweek1client19 = StringVar()
        friday_week1_client19= Entry(wrapper1frame, textvariable = fridayweek1client19, width = 12)
        friday_week1_client19.grid(column = 8, row = 21, padx = 5, pady = 5)

        fridayweek1client20 = StringVar()
        friday_week1_client20 = Entry(wrapper1frame, textvariable = fridayweek1client20, width = 12)
        friday_week1_client20.grid(column = 8, row = 22, padx = 5, pady = 5)

        #Client 1 field
        notes_client1 = StringVar()
        notes_client1_selection = Entry(wrapper1frame, textvariable = notes_client1, width = 12)
        notes_client1_selection.grid(column = 9, row = 3, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        notes_client2 = StringVar()
        notes_client2_selection = Entry(wrapper1frame, textvariable = notes_client2, width = 12)
        notes_client2_selection.grid(column = 9, row = 4, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        notes_client3 = StringVar()
        notes_client3_selection = Entry(wrapper1frame, textvariable = notes_client3, width = 12)
        notes_client3_selection.grid(column = 9, row = 5, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        notes_client4 = StringVar()
        notes_client4_selection = Entry(wrapper1frame, textvariable = notes_client4, width = 12)
        notes_client4_selection.grid(column = 9, row = 6, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        notes_client5 = StringVar()
        notes_client5_selection = Entry(wrapper1frame, textvariable = notes_client5, width = 12)
        notes_client5_selection.grid(column = 9, row = 7, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        notes_client6 = StringVar()
        notes_client6_selection = Entry(wrapper1frame, textvariable = notes_client6, width = 12)
        notes_client6_selection.grid(column = 9, row = 8, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        notes_client7 = StringVar()
        notes_client7_selection = Entry(wrapper1frame, textvariable = notes_client7, width = 12)
        notes_client7_selection.grid(column = 9, row = 9, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        notes_client8 = StringVar()
        notes_client8_selection = Entry(wrapper1frame, textvariable = notes_client8, width = 12)
        notes_client8_selection.grid(column = 9, row = 10, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        notes_client9 = StringVar()
        notes_client9_selection = Entry(wrapper1frame, textvariable = notes_client9, width = 12)
        notes_client9_selection.grid(column = 9, row = 11, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        notes_client10 = StringVar()
        notes_client10_selection = Entry(wrapper1frame, textvariable = notes_client10, width = 12)
        notes_client10_selection.grid(column = 9, row = 12, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        notes_client11 = StringVar()
        notes_client11_selection = Entry(wrapper1frame, textvariable = notes_client11, width = 12)
        notes_client11_selection.grid(column = 9, row = 13, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        notes_client12 = StringVar()
        notes_client12_selection = Entry(wrapper1frame, textvariable = notes_client12, width = 12)
        notes_client12_selection.grid(column = 9, row = 14, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        notes_client13 = StringVar()
        notes_client13_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client13_selection.grid(column = 9, row = 15, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        notes_client14 = StringVar()
        notes_client14_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client14_selection.grid(column = 9, row = 16, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        notes_client15 = StringVar()
        notes_client15_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client15_selection.grid(column = 9, row = 17, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        notes_client16 = StringVar()
        notes_client16_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client16_selection.grid(column = 9, row = 18, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        notes_client17 = StringVar()
        notes_client17_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client17_selection.grid(column = 9, row = 19, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        notes_client18 = StringVar()
        notes_client18_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client18_selection.grid(column = 9, row = 20, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        notes_client19 = StringVar()
        notes_client19_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client19_selection.grid(column = 9, row = 21, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        notes_client20 = StringVar()
        notes_client20_selection = Entry(wrapper1frame, textvariable = notes_client13, width = 12)
        notes_client20_selection.grid(column = 9, row = 22, columnspan = 1)

        notes_client1_notes = Button(wrapper1frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 22, sticky = "we", padx = 5, pady = 5)

        #Client 1 field
        engagementcode_client1 = StringVar()
        engagementcode_client1_selection = Entry(wrapper2frame, textvariable = engagementcode_client1, width = 12)
        engagementcode_client1_selection.grid(column = 0, row = 3, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        engagementcode_client2 = StringVar()
        engagementcode_client2_selection = Entry(wrapper2frame, textvariable = engagementcode_client2, width = 12)
        engagementcode_client2_selection.grid(column = 0, row = 4, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        engagementcode_client3 = StringVar()
        engagementcode_client3_selection = Entry(wrapper2frame, textvariable = engagementcode_client3, width = 12)
        engagementcode_client3_selection.grid(column = 0, row = 5, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        engagementcode_client4 = StringVar()
        engagementcode_client4_selection = Entry(wrapper2frame, textvariable = engagementcode_client4, width = 12)
        engagementcode_client4_selection.grid(column = 0, row = 6, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        engagementcode_client5 = StringVar()
        engagementcode_client5_selection = Entry(wrapper2frame, textvariable = engagementcode_client5, width = 12)
        engagementcode_client5_selection.grid(column = 0, row = 7, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        engagementcode_client6 = StringVar()
        engagementcode_client6_selection = Entry(wrapper2frame, textvariable = engagementcode_client6, width = 12)
        engagementcode_client6_selection.grid(column = 0, row = 8, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        engagementcode_client7 = StringVar()
        engagementcode_client7_selection = Entry(wrapper2frame, textvariable = engagementcode_client7, width = 12)
        engagementcode_client7_selection.grid(column = 0, row = 9, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        engagementcode_client8 = StringVar()
        engagementcode_client8_selection = Entry(wrapper2frame, textvariable = engagementcode_client8, width = 12)
        engagementcode_client8_selection.grid(column = 0, row = 10, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        engagementcode_client9 = StringVar()
        engagementcode_client9_selection = Entry(wrapper2frame, textvariable = engagementcode_client9, width = 12)
        engagementcode_client9_selection.grid(column = 0, row = 11, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        engagementcode_client10 = StringVar()
        engagementcode_client10_selection = Entry(wrapper2frame, textvariable = engagementcode_client10, width = 12)
        engagementcode_client10_selection.grid(column = 0, row = 12, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        engagementcode_client11 = StringVar()
        engagementcode_client11_selection = Entry(wrapper2frame, textvariable = engagementcode_client11, width = 12)
        engagementcode_client11_selection.grid(column = 0, row = 13, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        engagementcode_client12 = StringVar()
        engagementcode_client12_selection = Entry(wrapper2frame, textvariable = engagementcode_client12, width = 12)
        engagementcode_client12_selection.grid(column = 0, row = 14, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        engagementcode_client13 = StringVar()
        engagementcode_client13_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client13_selection.grid(column = 0, row = 15, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        engagementcode_client14 = StringVar()
        engagementcode_client14_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client14_selection.grid(column = 0, row = 16, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        engagementcode_client15 = StringVar()
        engagementcode_client15_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client15_selection.grid(column = 0, row = 17, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        engagementcode_client16 = StringVar()
        engagementcode_client16_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client16_selection.grid(column = 0, row = 18, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        engagementcode_client17 = StringVar()
        engagementcode_client17_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client17_selection.grid(column = 0, row = 19, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        engagementcode_client18 = StringVar()
        engagementcode_client18_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client18_selection.grid(column = 0, row = 20, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        engagementcode_client19 = StringVar()
        engagementcode_client19_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client19_selection.grid(column = 0, row = 21, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        engagementcode_client20 = StringVar()
        engagementcode_client20_selection = Entry(wrapper2frame, textvariable = engagementcode_client13, width = 12)
        engagementcode_client20_selection.grid(column = 0, row = 22, columnspan = 1)

        engagementcode_client1_search = Button(wrapper2frame, image = search_icon_resize)
        engagementcode_client1_search.grid(column = 1, row = 22, sticky = "we", padx = 5, pady = 5)

        #Weekday hours field example
        saturdayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = saturdayweek1, width = 12)
        week1_label.grid(column = 2, row = 2, padx = 5, pady = 5)

        saturdayweek1client1 = StringVar()
        saturday_week1_client1 = Entry(wrapper2frame, textvariable = saturdayweek1client1, width = 12)
        saturday_week1_client1.grid(column = 2, row = 3, padx = 5, pady = 5)

        saturdayweek1client2 = StringVar()
        saturday_week1_client2 = Entry(wrapper2frame, textvariable = saturdayweek1client2, width = 12)
        saturday_week1_client2.grid(column = 2, row = 4, padx = 5, pady = 5)

        saturdayweek1client3 = StringVar()
        saturday_week1_client3 = Entry(wrapper2frame, textvariable = saturdayweek1client3, width = 12)
        saturday_week1_client3.grid(column = 2, row = 5, padx = 5, pady = 5)

        saturdayweek1client4 = StringVar()
        saturday_week1_client4 = Entry(wrapper2frame, textvariable = saturdayweek1client4, width = 12)
        saturday_week1_client4.grid(column = 2, row = 6, padx = 5, pady = 5)

        saturdayweek1client5 = StringVar()
        saturday_week1_client5 = Entry(wrapper2frame, textvariable = saturdayweek1client5, width = 12)
        saturday_week1_client5.grid(column = 2, row = 7, padx = 5, pady = 5)

        saturdayweek1client6 = StringVar()
        saturday_week1_client6 = Entry(wrapper2frame, textvariable = saturdayweek1client6, width = 12)
        saturday_week1_client6.grid(column = 2, row = 8, padx = 5, pady = 5)

        saturdayweek1client7 = StringVar()
        saturday_week1_client7 = Entry(wrapper2frame, textvariable = saturdayweek1client7, width = 12)
        saturday_week1_client7.grid(column = 2, row = 9, padx = 5, pady = 5)

        saturdayweek1client8 = StringVar()
        saturday_week1_client8 = Entry(wrapper2frame, textvariable = saturdayweek1client8, width = 12)
        saturday_week1_client8.grid(column = 2, row = 10, padx = 5, pady = 5)

        saturdayweek1client9 = StringVar()
        saturday_week1_client9 = Entry(wrapper2frame, textvariable = saturdayweek1client9, width = 12)
        saturday_week1_client9.grid(column = 2, row = 11, padx = 5, pady = 5)

        saturdayweek1client10 = StringVar()
        saturday_week1_client10 = Entry(wrapper2frame, textvariable = saturdayweek1client10, width = 12)
        saturday_week1_client10.grid(column = 2, row = 12, padx = 5, pady = 5)

        saturdayweek1client11 = StringVar()
        saturday_week1_client11 = Entry(wrapper2frame, textvariable = saturdayweek1client11, width = 12)
        saturday_week1_client11.grid(column = 2, row = 13, padx = 5, pady = 5)

        saturdayweek1client12 = StringVar()
        saturday_week1_client12 = Entry(wrapper2frame, textvariable = saturdayweek1client12, width = 12)
        saturday_week1_client12.grid(column = 2, row = 14, padx = 5, pady = 5)

        saturdayweek1client13 = StringVar()
        saturday_week1_client13 = Entry(wrapper2frame, textvariable = saturdayweek1client13, width = 12)
        saturday_week1_client13.grid(column = 2, row = 15, padx = 5, pady = 5)

        saturdayweek1client14 = StringVar()
        saturday_week1_client14 = Entry(wrapper2frame, textvariable = saturdayweek1client14, width = 12)
        saturday_week1_client14.grid(column = 2, row = 16, padx = 5, pady = 5)

        saturdayweek1client15 = StringVar()
        saturday_week1_client15 = Entry(wrapper2frame, textvariable = saturdayweek1client15, width = 12)
        saturday_week1_client15.grid(column = 2, row = 17, padx = 5, pady = 5)

        saturdayweek1client16 = StringVar()
        saturday_week1_client16 = Entry(wrapper2frame, textvariable = saturdayweek1client16, width = 12)
        saturday_week1_client16.grid(column = 2, row = 18, padx = 5, pady = 5)

        saturdayweek1client17 = StringVar()
        saturday_week1_client17 = Entry(wrapper2frame, textvariable = saturdayweek1client17, width = 12)
        saturday_week1_client17.grid(column = 2, row = 19, padx = 5, pady = 5)

        saturdayweek1client18 = StringVar()
        saturday_week1_client18 = Entry(wrapper2frame, textvariable = saturdayweek1client18, width = 12)
        saturday_week1_client18.grid(column = 2, row = 20, padx = 5, pady = 5)

        saturdayweek1client19 = StringVar()
        saturday_week1_client19= Entry(wrapper2frame, textvariable = saturdayweek1client19, width = 12)
        saturday_week1_client19.grid(column = 2, row = 21, padx = 5, pady = 5)

        saturdayweek1client20 = StringVar()
        saturday_week1_client20 = Entry(wrapper2frame, textvariable = saturdayweek1client20, width = 12)
        saturday_week1_client20.grid(column = 2, row = 22, padx = 5, pady = 5)

        sundayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = sundayweek1, width = 12)
        week1_label.grid(column = 3, row = 2, padx = 5, pady = 5)

        sundayweek1client1 = StringVar()
        sunday_week1_client1 = Entry(wrapper2frame, textvariable = sundayweek1client1, width = 12)
        sunday_week1_client1.grid(column = 3, row = 3, padx = 5, pady = 5)

        sundayweek1client2 = StringVar()
        sunday_week1_client2 = Entry(wrapper2frame, textvariable = sundayweek1client2, width = 12)
        sunday_week1_client2.grid(column = 3, row = 4, padx = 5, pady = 5)

        sundayweek1client3 = StringVar()
        sunday_week1_client3 = Entry(wrapper2frame, textvariable = sundayweek1client3, width = 12)
        sunday_week1_client3.grid(column = 3, row = 5, padx = 5, pady = 5)

        sundayweek1client4 = StringVar()
        sunday_week1_client4 = Entry(wrapper2frame, textvariable = sundayweek1client4, width = 12)
        sunday_week1_client4.grid(column = 3, row = 6, padx = 5, pady = 5)

        sundayweek1client5 = StringVar()
        sunday_week1_client5 = Entry(wrapper2frame, textvariable = sundayweek1client5, width = 12)
        sunday_week1_client5.grid(column = 3, row = 7, padx = 5, pady = 5)

        sundayweek1client6 = StringVar()
        sunday_week1_client6 = Entry(wrapper2frame, textvariable = sundayweek1client6, width = 12)
        sunday_week1_client6.grid(column = 3, row = 8, padx = 5, pady = 5)

        sundayweek1client7 = StringVar()
        sunday_week1_client7 = Entry(wrapper2frame, textvariable = sundayweek1client7, width = 12)
        sunday_week1_client7.grid(column = 3, row = 9, padx = 5, pady = 5)

        sundayweek1client8 = StringVar()
        sunday_week1_client8 = Entry(wrapper2frame, textvariable = sundayweek1client8, width = 12)
        sunday_week1_client8.grid(column = 3, row = 10, padx = 5, pady = 5)

        sundayweek1client9 = StringVar()
        sunday_week1_client9 = Entry(wrapper2frame, textvariable = sundayweek1client9, width = 12)
        sunday_week1_client9.grid(column = 3, row = 11, padx = 5, pady = 5)

        sundayweek1client10 = StringVar()
        sunday_week1_client10 = Entry(wrapper2frame, textvariable = sundayweek1client10, width = 12)
        sunday_week1_client10.grid(column = 3, row = 12, padx = 5, pady = 5)

        sundayweek1client11 = StringVar()
        sunday_week1_client11 = Entry(wrapper2frame, textvariable = sundayweek1client11, width = 12)
        sunday_week1_client11.grid(column = 3, row = 13, padx = 5, pady = 5)

        sundayweek1client12 = StringVar()
        sunday_week1_client12 = Entry(wrapper2frame, textvariable = sundayweek1client12, width = 12)
        sunday_week1_client12.grid(column = 3, row = 14, padx = 5, pady = 5)

        sundayweek1client13 = StringVar()
        sunday_week1_client13 = Entry(wrapper2frame, textvariable = sundayweek1client13, width = 12)
        sunday_week1_client13.grid(column = 3, row = 15, padx = 5, pady = 5)

        sundayweek1client14 = StringVar()
        sunday_week1_client14 = Entry(wrapper2frame, textvariable = sundayweek1client14, width = 12)
        sunday_week1_client14.grid(column = 3, row = 16, padx = 5, pady = 5)

        sundayweek1client15 = StringVar()
        sunday_week1_client15 = Entry(wrapper2frame, textvariable = sundayweek1client15, width = 12)
        sunday_week1_client15.grid(column = 3, row = 17, padx = 5, pady = 5)

        sundayweek1client16 = StringVar()
        sunday_week1_client16 = Entry(wrapper2frame, textvariable = sundayweek1client16, width = 12)
        sunday_week1_client16.grid(column = 3, row = 18, padx = 5, pady = 5)

        sundayweek1client17 = StringVar()
        sunday_week1_client17 = Entry(wrapper2frame, textvariable = sundayweek1client17, width = 12)
        sunday_week1_client17.grid(column = 3, row = 19, padx = 5, pady = 5)

        sundayweek1client18 = StringVar()
        sunday_week1_client18 = Entry(wrapper2frame, textvariable = sundayweek1client18, width = 12)
        sunday_week1_client18.grid(column = 3, row = 20, padx = 5, pady = 5)

        sundayweek1client19 = StringVar()
        sunday_week1_client19= Entry(wrapper2frame, textvariable = sundayweek1client19, width = 12)
        sunday_week1_client19.grid(column = 3, row = 21, padx = 5, pady = 5)

        sundayweek1client20 = StringVar()
        sunday_week1_client20 = Entry(wrapper2frame, textvariable = sundayweek1client20, width = 12)
        sunday_week1_client20.grid(column = 3, row = 22, padx = 5, pady = 5)

        mondayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = mondayweek1, width = 12)
        week1_label.grid(column = 4, row = 2, padx = 5, pady = 5)

        mondayweek1client1 = StringVar()
        monday_week1_client1 = Entry(wrapper2frame, textvariable = mondayweek1client1, width = 12)
        monday_week1_client1.grid(column = 4, row = 3, padx = 5, pady = 5)

        mondayweek1client2 = StringVar()
        monday_week1_client2 = Entry(wrapper2frame, textvariable = mondayweek1client2, width = 12)
        monday_week1_client2.grid(column = 4, row = 4, padx = 5, pady = 5)

        mondayweek1client3 = StringVar()
        monday_week1_client3 = Entry(wrapper2frame, textvariable = mondayweek1client3, width = 12)
        monday_week1_client3.grid(column = 4, row = 5, padx = 5, pady = 5)

        mondayweek1client4 = StringVar()
        monday_week1_client4 = Entry(wrapper2frame, textvariable = mondayweek1client4, width = 12)
        monday_week1_client4.grid(column = 4, row = 6, padx = 5, pady = 5)

        mondayweek1client5 = StringVar()
        monday_week1_client5 = Entry(wrapper2frame, textvariable = mondayweek1client5, width = 12)
        monday_week1_client5.grid(column = 4, row = 7, padx = 5, pady = 5)

        mondayweek1client6 = StringVar()
        monday_week1_client6 = Entry(wrapper2frame, textvariable = mondayweek1client6, width = 12)
        monday_week1_client6.grid(column = 4, row = 8, padx = 5, pady = 5)

        mondayweek1client7 = StringVar()
        monday_week1_client7 = Entry(wrapper2frame, textvariable = mondayweek1client7, width = 12)
        monday_week1_client7.grid(column = 4, row = 9, padx = 5, pady = 5)

        mondayweek1client8 = StringVar()
        monday_week1_client8 = Entry(wrapper2frame, textvariable = mondayweek1client8, width = 12)
        monday_week1_client8.grid(column = 4, row = 10, padx = 5, pady = 5)

        mondayweek1client9 = StringVar()
        monday_week1_client9 = Entry(wrapper2frame, textvariable = mondayweek1client9, width = 12)
        monday_week1_client9.grid(column = 4, row = 11, padx = 5, pady = 5)

        mondayweek1client10 = StringVar()
        monday_week1_client10 = Entry(wrapper2frame, textvariable = mondayweek1client10, width = 12)
        monday_week1_client10.grid(column = 4, row = 12, padx = 5, pady = 5)

        mondayweek1client11 = StringVar()
        monday_week1_client11 = Entry(wrapper2frame, textvariable = mondayweek1client11, width = 12)
        monday_week1_client11.grid(column = 4, row = 13, padx = 5, pady = 5)

        mondayweek1client12 = StringVar()
        monday_week1_client12 = Entry(wrapper2frame, textvariable = mondayweek1client12, width = 12)
        monday_week1_client12.grid(column = 4, row = 14, padx = 5, pady = 5)

        mondayweek1client13 = StringVar()
        monday_week1_client13 = Entry(wrapper2frame, textvariable = mondayweek1client13, width = 12)
        monday_week1_client13.grid(column = 4, row = 15, padx = 5, pady = 5)

        mondayweek1client14 = StringVar()
        monday_week1_client14 = Entry(wrapper2frame, textvariable = mondayweek1client14, width = 12)
        monday_week1_client14.grid(column = 4, row = 16, padx = 5, pady = 5)

        mondayweek1client15 = StringVar()
        monday_week1_client15 = Entry(wrapper2frame, textvariable = mondayweek1client15, width = 12)
        monday_week1_client15.grid(column = 4, row = 17, padx = 5, pady = 5)

        mondayweek1client16 = StringVar()
        monday_week1_client16 = Entry(wrapper2frame, textvariable = mondayweek1client16, width = 12)
        monday_week1_client16.grid(column = 4, row = 18, padx = 5, pady = 5)

        mondayweek1client17 = StringVar()
        monday_week1_client17 = Entry(wrapper2frame, textvariable = mondayweek1client17, width = 12)
        monday_week1_client17.grid(column = 4, row = 19, padx = 5, pady = 5)

        mondayweek1client18 = StringVar()
        monday_week1_client18 = Entry(wrapper2frame, textvariable = mondayweek1client18, width = 12)
        monday_week1_client18.grid(column = 4, row = 20, padx = 5, pady = 5)

        mondayweek1client19 = StringVar()
        monday_week1_client19= Entry(wrapper2frame, textvariable = mondayweek1client19, width = 12)
        monday_week1_client19.grid(column = 4, row = 21, padx = 5, pady = 5)

        mondayweek1client20 = StringVar()
        monday_week1_client20 = Entry(wrapper2frame, textvariable = mondayweek1client20, width = 12)
        monday_week1_client20.grid(column = 4, row = 22, padx = 5, pady = 5)

        tuesdayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = tuesdayweek1, width = 12)
        week1_label.grid(column = 5, row = 2, padx = 5, pady = 5)

        tuesdayweek1client1 = StringVar()
        tuesday_week1_client1 = Entry(wrapper2frame, textvariable = tuesdayweek1client1, width = 12)
        tuesday_week1_client1.grid(column = 5, row = 3, padx = 5, pady = 5)

        tuesdayweek1client2 = StringVar()
        tuesday_week1_client2 = Entry(wrapper2frame, textvariable = tuesdayweek1client2, width = 12)
        tuesday_week1_client2.grid(column = 5, row = 4, padx = 5, pady = 5)

        tuesdayweek1client3 = StringVar()
        tuesday_week1_client3 = Entry(wrapper2frame, textvariable = tuesdayweek1client3, width = 12)
        tuesday_week1_client3.grid(column = 5, row = 5, padx = 5, pady = 5)

        tuesdayweek1client4 = StringVar()
        tuesday_week1_client4 = Entry(wrapper2frame, textvariable = tuesdayweek1client4, width = 12)
        tuesday_week1_client4.grid(column = 5, row = 6, padx = 5, pady = 5)

        tuesdayweek1client5 = StringVar()
        tuesday_week1_client5 = Entry(wrapper2frame, textvariable = tuesdayweek1client5, width = 12)
        tuesday_week1_client5.grid(column = 5, row = 7, padx = 5, pady = 5)

        tuesdayweek1client6 = StringVar()
        tuesday_week1_client6 = Entry(wrapper2frame, textvariable = tuesdayweek1client6, width = 12)
        tuesday_week1_client6.grid(column = 5, row = 8, padx = 5, pady = 5)

        tuesdayweek1client7 = StringVar()
        tuesday_week1_client7 = Entry(wrapper2frame, textvariable = tuesdayweek1client7, width = 12)
        tuesday_week1_client7.grid(column = 5, row = 9, padx = 5, pady = 5)

        tuesdayweek1client8 = StringVar()
        tuesday_week1_client8 = Entry(wrapper2frame, textvariable = tuesdayweek1client8, width = 12)
        tuesday_week1_client8.grid(column = 5, row = 10, padx = 5, pady = 5)

        tuesdayweek1client9 = StringVar()
        tuesday_week1_client9 = Entry(wrapper2frame, textvariable = tuesdayweek1client9, width = 12)
        tuesday_week1_client9.grid(column = 5, row = 11, padx = 5, pady = 5)

        tuesdayweek1client10 = StringVar()
        tuesday_week1_client10 = Entry(wrapper2frame, textvariable = tuesdayweek1client10, width = 12)
        tuesday_week1_client10.grid(column = 5, row = 12, padx = 5, pady = 5)

        tuesdayweek1client11 = StringVar()
        tuesday_week1_client11 = Entry(wrapper2frame, textvariable = tuesdayweek1client11, width = 12)
        tuesday_week1_client11.grid(column = 5, row = 13, padx = 5, pady = 5)

        tuesdayweek1client12 = StringVar()
        tuesday_week1_client12 = Entry(wrapper2frame, textvariable = tuesdayweek1client12, width = 12)
        tuesday_week1_client12.grid(column = 5, row = 14, padx = 5, pady = 5)

        tuesdayweek1client13 = StringVar()
        tuesday_week1_client13 = Entry(wrapper2frame, textvariable = tuesdayweek1client13, width = 12)
        tuesday_week1_client13.grid(column = 5, row = 15, padx = 5, pady = 5)

        tuesdayweek1client14 = StringVar()
        tuesday_week1_client14 = Entry(wrapper2frame, textvariable = tuesdayweek1client14, width = 12)
        tuesday_week1_client14.grid(column = 5, row = 16, padx = 5, pady = 5)

        tuesdayweek1client15 = StringVar()
        tuesday_week1_client15 = Entry(wrapper2frame, textvariable = tuesdayweek1client15, width = 12)
        tuesday_week1_client15.grid(column = 5, row = 17, padx = 5, pady = 5)

        tuesdayweek1client16 = StringVar()
        tuesday_week1_client16 = Entry(wrapper2frame, textvariable = tuesdayweek1client16, width = 12)
        tuesday_week1_client16.grid(column = 5, row = 18, padx = 5, pady = 5)

        tuesdayweek1client17 = StringVar()
        tuesday_week1_client17 = Entry(wrapper2frame, textvariable = tuesdayweek1client17, width = 12)
        tuesday_week1_client17.grid(column = 5, row = 19, padx = 5, pady = 5)

        tuesdayweek1client18 = StringVar()
        tuesday_week1_client18 = Entry(wrapper2frame, textvariable = tuesdayweek1client18, width = 12)
        tuesday_week1_client18.grid(column = 5, row = 20, padx = 5, pady = 5)

        tuesdayweek1client19 = StringVar()
        tuesday_week1_client19= Entry(wrapper2frame, textvariable = tuesdayweek1client19, width = 12)
        tuesday_week1_client19.grid(column = 5, row = 21, padx = 5, pady = 5)

        tuesdayweek1client20 = StringVar()
        tuesday_week1_client20 = Entry(wrapper2frame, textvariable = tuesdayweek1client20, width = 12)
        tuesday_week1_client20.grid(column = 5, row = 22, padx = 5, pady = 5)

        wednesdayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = wednesdayweek1, width = 12)
        week1_label.grid(column = 6, row = 2, padx = 5, pady = 5)

        wednesdayweek1client1 = StringVar()
        wednesday_week1_client1 = Entry(wrapper2frame, textvariable = wednesdayweek1client1, width = 12)
        wednesday_week1_client1.grid(column = 6, row = 3, padx = 5, pady = 5)

        wednesdayweek1client2 = StringVar()
        wednesday_week1_client2 = Entry(wrapper2frame, textvariable = wednesdayweek1client2, width = 12)
        wednesday_week1_client2.grid(column = 6, row = 4, padx = 5, pady = 5)

        wednesdayweek1client3 = StringVar()
        wednesday_week1_client3 = Entry(wrapper2frame, textvariable = wednesdayweek1client3, width = 12)
        wednesday_week1_client3.grid(column = 6, row = 5, padx = 5, pady = 5)

        wednesdayweek1client4 = StringVar()
        wednesday_week1_client4 = Entry(wrapper2frame, textvariable = wednesdayweek1client4, width = 12)
        wednesday_week1_client4.grid(column = 6, row = 6, padx = 5, pady = 5)

        wednesdayweek1client5 = StringVar()
        wednesday_week1_client5 = Entry(wrapper2frame, textvariable = wednesdayweek1client5, width = 12)
        wednesday_week1_client5.grid(column = 6, row = 7, padx = 5, pady = 5)

        wednesdayweek1client6 = StringVar()
        wednesday_week1_client6 = Entry(wrapper2frame, textvariable = wednesdayweek1client6, width = 12)
        wednesday_week1_client6.grid(column = 6, row = 8, padx = 5, pady = 5)

        wednesdayweek1client7 = StringVar()
        wednesday_week1_client7 = Entry(wrapper2frame, textvariable = wednesdayweek1client7, width = 12)
        wednesday_week1_client7.grid(column = 6, row = 9, padx = 5, pady = 5)

        wednesdayweek1client8 = StringVar()
        wednesday_week1_client8 = Entry(wrapper2frame, textvariable = wednesdayweek1client8, width = 12)
        wednesday_week1_client8.grid(column = 6, row = 10, padx = 5, pady = 5)

        wednesdayweek1client9 = StringVar()
        wednesday_week1_client9 = Entry(wrapper2frame, textvariable = wednesdayweek1client9, width = 12)
        wednesday_week1_client9.grid(column = 6, row = 11, padx = 5, pady = 5)

        wednesdayweek1client10 = StringVar()
        wednesday_week1_client10 = Entry(wrapper2frame, textvariable = wednesdayweek1client10, width = 12)
        wednesday_week1_client10.grid(column = 6, row = 12, padx = 5, pady = 5)

        wednesdayweek1client11 = StringVar()
        wednesday_week1_client11 = Entry(wrapper2frame, textvariable = wednesdayweek1client11, width = 12)
        wednesday_week1_client11.grid(column = 6, row = 13, padx = 5, pady = 5)

        wednesdayweek1client12 = StringVar()
        wednesday_week1_client12 = Entry(wrapper2frame, textvariable = wednesdayweek1client12, width = 12)
        wednesday_week1_client12.grid(column = 6, row = 14, padx = 5, pady = 5)

        wednesdayweek1client13 = StringVar()
        wednesday_week1_client13 = Entry(wrapper2frame, textvariable = wednesdayweek1client13, width = 12)
        wednesday_week1_client13.grid(column = 6, row = 15, padx = 5, pady = 5)

        wednesdayweek1client14 = StringVar()
        wednesday_week1_client14 = Entry(wrapper2frame, textvariable = wednesdayweek1client14, width = 12)
        wednesday_week1_client14.grid(column = 6, row = 16, padx = 5, pady = 5)

        wednesdayweek1client15 = StringVar()
        wednesday_week1_client15 = Entry(wrapper2frame, textvariable = wednesdayweek1client15, width = 12)
        wednesday_week1_client15.grid(column = 6, row = 17, padx = 5, pady = 5)

        wednesdayweek1client16 = StringVar()
        wednesday_week1_client16 = Entry(wrapper2frame, textvariable = wednesdayweek1client16, width = 12)
        wednesday_week1_client16.grid(column = 6, row = 18, padx = 5, pady = 5)

        wednesdayweek1client17 = StringVar()
        wednesday_week1_client17 = Entry(wrapper2frame, textvariable = wednesdayweek1client17, width = 12)
        wednesday_week1_client17.grid(column = 6, row = 19, padx = 5, pady = 5)

        wednesdayweek1client18 = StringVar()
        wednesday_week1_client18 = Entry(wrapper2frame, textvariable = wednesdayweek1client18, width = 12)
        wednesday_week1_client18.grid(column = 6, row = 20, padx = 5, pady = 5)

        wednesdayweek1client19 = StringVar()
        wednesday_week1_client19= Entry(wrapper2frame, textvariable = wednesdayweek1client19, width = 12)
        wednesday_week1_client19.grid(column = 6, row = 21, padx = 5, pady = 5)

        wednesdayweek1client20 = StringVar()
        wednesday_week1_client20 = Entry(wrapper2frame, textvariable = wednesdayweek1client20, width = 12)
        wednesday_week1_client20.grid(column = 6, row = 22, padx = 5, pady = 5)

        thursdayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = thursdayweek1, width = 12)
        week1_label.grid(column = 7, row = 2, padx = 5, pady = 5)

        thursdayweek1client1 = StringVar()
        thursday_week1_client1 = Entry(wrapper2frame, textvariable = thursdayweek1client1, width = 12)
        thursday_week1_client1.grid(column = 7, row = 3, padx = 5, pady = 5)

        thursdayweek1client2 = StringVar()
        thursday_week1_client2 = Entry(wrapper2frame, textvariable = thursdayweek1client2, width = 12)
        thursday_week1_client2.grid(column = 7, row = 4, padx = 5, pady = 5)

        thursdayweek1client3 = StringVar()
        thursday_week1_client3 = Entry(wrapper2frame, textvariable = thursdayweek1client3, width = 12)
        thursday_week1_client3.grid(column = 7, row = 5, padx = 5, pady = 5)

        thursdayweek1client4 = StringVar()
        thursday_week1_client4 = Entry(wrapper2frame, textvariable = thursdayweek1client4, width = 12)
        thursday_week1_client4.grid(column = 7, row = 6, padx = 5, pady = 5)

        thursdayweek1client5 = StringVar()
        thursday_week1_client5 = Entry(wrapper2frame, textvariable = thursdayweek1client5, width = 12)
        thursday_week1_client5.grid(column = 7, row = 7, padx = 5, pady = 5)

        thursdayweek1client6 = StringVar()
        thursday_week1_client6 = Entry(wrapper2frame, textvariable = thursdayweek1client6, width = 12)
        thursday_week1_client6.grid(column = 7, row = 8, padx = 5, pady = 5)

        thursdayweek1client7 = StringVar()
        thursday_week1_client7 = Entry(wrapper2frame, textvariable = thursdayweek1client7, width = 12)
        thursday_week1_client7.grid(column = 7, row = 9, padx = 5, pady = 5)

        thursdayweek1client8 = StringVar()
        thursday_week1_client8 = Entry(wrapper2frame, textvariable = thursdayweek1client8, width = 12)
        thursday_week1_client8.grid(column = 7, row = 10, padx = 5, pady = 5)

        thursdayweek1client9 = StringVar()
        thursday_week1_client9 = Entry(wrapper2frame, textvariable = thursdayweek1client9, width = 12)
        thursday_week1_client9.grid(column = 7, row = 11, padx = 5, pady = 5)

        thursdayweek1client10 = StringVar()
        thursday_week1_client10 = Entry(wrapper2frame, textvariable = thursdayweek1client10, width = 12)
        thursday_week1_client10.grid(column = 7, row = 12, padx = 5, pady = 5)

        thursdayweek1client11 = StringVar()
        thursday_week1_client11 = Entry(wrapper2frame, textvariable = thursdayweek1client11, width = 12)
        thursday_week1_client11.grid(column = 7, row = 13, padx = 5, pady = 5)

        thursdayweek1client12 = StringVar()
        thursday_week1_client12 = Entry(wrapper2frame, textvariable = thursdayweek1client12, width = 12)
        thursday_week1_client12.grid(column = 7, row = 14, padx = 5, pady = 5)

        thursdayweek1client13 = StringVar()
        thursday_week1_client13 = Entry(wrapper2frame, textvariable = thursdayweek1client13, width = 12)
        thursday_week1_client13.grid(column = 7, row = 15, padx = 5, pady = 5)

        thursdayweek1client14 = StringVar()
        thursday_week1_client14 = Entry(wrapper2frame, textvariable = thursdayweek1client14, width = 12)
        thursday_week1_client14.grid(column = 7, row = 16, padx = 5, pady = 5)

        thursdayweek1client15 = StringVar()
        thursday_week1_client15 = Entry(wrapper2frame, textvariable = thursdayweek1client15, width = 12)
        thursday_week1_client15.grid(column = 7, row = 17, padx = 5, pady = 5)

        thursdayweek1client16 = StringVar()
        thursday_week1_client16 = Entry(wrapper2frame, textvariable = thursdayweek1client16, width = 12)
        thursday_week1_client16.grid(column = 7, row = 18, padx = 5, pady = 5)

        thursdayweek1client17 = StringVar()
        thursday_week1_client17 = Entry(wrapper2frame, textvariable = thursdayweek1client17, width = 12)
        thursday_week1_client17.grid(column = 7, row = 19, padx = 5, pady = 5)

        thursdayweek1client18 = StringVar()
        thursday_week1_client18 = Entry(wrapper2frame, textvariable = thursdayweek1client18, width = 12)
        thursday_week1_client18.grid(column = 7, row = 20, padx = 5, pady = 5)

        thursdayweek1client19 = StringVar()
        thursday_week1_client19= Entry(wrapper2frame, textvariable = thursdayweek1client19, width = 12)
        thursday_week1_client19.grid(column = 7, row = 21, padx = 5, pady = 5)

        thursdayweek1client20 = StringVar()
        thursday_week1_client20 = Entry(wrapper2frame, textvariable = thursdayweek1client20, width = 12)
        thursday_week1_client20.grid(column = 7, row = 22, padx = 5, pady = 5)

        fridayweek1 = StringVar()
        week1_label = Entry(wrapper2frame, textvariable = fridayweek1, width = 12)
        week1_label.grid(column = 8, row = 2, padx = 5, pady = 5)

        fridayweek1client1 = StringVar()
        friday_week1_client1 = Entry(wrapper2frame, textvariable = fridayweek1client1, width = 12)
        friday_week1_client1.grid(column = 8, row = 3, padx = 5, pady = 5)

        fridayweek1client2 = StringVar()
        friday_week1_client2 = Entry(wrapper2frame, textvariable = fridayweek1client2, width = 12)
        friday_week1_client2.grid(column = 8, row = 4, padx = 5, pady = 5)

        fridayweek1client3 = StringVar()
        friday_week1_client3 = Entry(wrapper2frame, textvariable = fridayweek1client3, width = 12)
        friday_week1_client3.grid(column = 8, row = 5, padx = 5, pady = 5)

        fridayweek1client4 = StringVar()
        friday_week1_client4 = Entry(wrapper2frame, textvariable = fridayweek1client4, width = 12)
        friday_week1_client4.grid(column = 8, row = 6, padx = 5, pady = 5)

        fridayweek1client5 = StringVar()
        friday_week1_client5 = Entry(wrapper2frame, textvariable = fridayweek1client5, width = 12)
        friday_week1_client5.grid(column = 8, row = 7, padx = 5, pady = 5)

        fridayweek1client6 = StringVar()
        friday_week1_client6 = Entry(wrapper2frame, textvariable = fridayweek1client6, width = 12)
        friday_week1_client6.grid(column = 8, row = 8, padx = 5, pady = 5)

        fridayweek1client7 = StringVar()
        friday_week1_client7 = Entry(wrapper2frame, textvariable = fridayweek1client7, width = 12)
        friday_week1_client7.grid(column = 8, row = 9, padx = 5, pady = 5)

        fridayweek1client8 = StringVar()
        friday_week1_client8 = Entry(wrapper2frame, textvariable = fridayweek1client8, width = 12)
        friday_week1_client8.grid(column = 8, row = 10, padx = 5, pady = 5)

        fridayweek1client9 = StringVar()
        friday_week1_client9 = Entry(wrapper2frame, textvariable = fridayweek1client9, width = 12)
        friday_week1_client9.grid(column = 8, row = 11, padx = 5, pady = 5)

        fridayweek1client10 = StringVar()
        friday_week1_client10 = Entry(wrapper2frame, textvariable = fridayweek1client10, width = 12)
        friday_week1_client10.grid(column = 8, row = 12, padx = 5, pady = 5)

        fridayweek1client11 = StringVar()
        friday_week1_client11 = Entry(wrapper2frame, textvariable = fridayweek1client11, width = 12)
        friday_week1_client11.grid(column = 8, row = 13, padx = 5, pady = 5)

        fridayweek1client12 = StringVar()
        friday_week1_client12 = Entry(wrapper2frame, textvariable = fridayweek1client12, width = 12)
        friday_week1_client12.grid(column = 8, row = 14, padx = 5, pady = 5)

        fridayweek1client13 = StringVar()
        friday_week1_client13 = Entry(wrapper2frame, textvariable = fridayweek1client13, width = 12)
        friday_week1_client13.grid(column = 8, row = 15, padx = 5, pady = 5)

        fridayweek1client14 = StringVar()
        friday_week1_client14 = Entry(wrapper2frame, textvariable = fridayweek1client14, width = 12)
        friday_week1_client14.grid(column = 8, row = 16, padx = 5, pady = 5)

        fridayweek1client15 = StringVar()
        friday_week1_client15 = Entry(wrapper2frame, textvariable = fridayweek1client15, width = 12)
        friday_week1_client15.grid(column = 8, row = 17, padx = 5, pady = 5)

        fridayweek1client16 = StringVar()
        friday_week1_client16 = Entry(wrapper2frame, textvariable = fridayweek1client16, width = 12)
        friday_week1_client16.grid(column = 8, row = 18, padx = 5, pady = 5)

        fridayweek1client17 = StringVar()
        friday_week1_client17 = Entry(wrapper2frame, textvariable = fridayweek1client17, width = 12)
        friday_week1_client17.grid(column = 8, row = 19, padx = 5, pady = 5)

        fridayweek1client18 = StringVar()
        friday_week1_client18 = Entry(wrapper2frame, textvariable = fridayweek1client18, width = 12)
        friday_week1_client18.grid(column = 8, row = 20, padx = 5, pady = 5)

        fridayweek1client19 = StringVar()
        friday_week1_client19= Entry(wrapper2frame, textvariable = fridayweek1client19, width = 12)
        friday_week1_client19.grid(column = 8, row = 21, padx = 5, pady = 5)

        fridayweek1client20 = StringVar()
        friday_week1_client20 = Entry(wrapper2frame, textvariable = fridayweek1client20, width = 12)
        friday_week1_client20.grid(column = 8, row = 22, padx = 5, pady = 5)

        #Client 1 field
        notes_client1 = StringVar()
        notes_client1_selection = Entry(wrapper2frame, textvariable = notes_client1, width = 12)
        notes_client1_selection.grid(column = 9, row = 3, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 3, sticky = "we", padx = 5, pady = 5)

        #Client 2 field
        notes_client2 = StringVar()
        notes_client2_selection = Entry(wrapper2frame, textvariable = notes_client2, width = 12)
        notes_client2_selection.grid(column = 9, row = 4, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 4, sticky = "we", padx = 5, pady = 5)

        #Client 3 field
        notes_client3 = StringVar()
        notes_client3_selection = Entry(wrapper2frame, textvariable = notes_client3, width = 12)
        notes_client3_selection.grid(column = 9, row = 5, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 5, sticky = "we", padx = 5, pady = 5)

        #Client 4 field
        notes_client4 = StringVar()
        notes_client4_selection = Entry(wrapper2frame, textvariable = notes_client4, width = 12)
        notes_client4_selection.grid(column = 9, row = 6, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 6, sticky = "we", padx = 5, pady = 5)

        #Client 5 field
        notes_client5 = StringVar()
        notes_client5_selection = Entry(wrapper2frame, textvariable = notes_client5, width = 12)
        notes_client5_selection.grid(column = 9, row = 7, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 7, sticky = "we", padx = 5, pady = 5)

        #Client 6 field
        notes_client6 = StringVar()
        notes_client6_selection = Entry(wrapper2frame, textvariable = notes_client6, width = 12)
        notes_client6_selection.grid(column = 9, row = 8, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 8, sticky = "we", padx = 5, pady = 5)

        #Client 7 field
        notes_client7 = StringVar()
        notes_client7_selection = Entry(wrapper2frame, textvariable = notes_client7, width = 12)
        notes_client7_selection.grid(column = 9, row = 9, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 9, sticky = "we", padx = 5, pady = 5)

        #Client 8 field
        notes_client8 = StringVar()
        notes_client8_selection = Entry(wrapper2frame, textvariable = notes_client8, width = 12)
        notes_client8_selection.grid(column = 9, row = 10, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 10, sticky = "we", padx = 5, pady = 5)

        #Client 9 field
        notes_client9 = StringVar()
        notes_client9_selection = Entry(wrapper2frame, textvariable = notes_client9, width = 12)
        notes_client9_selection.grid(column = 9, row = 11, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 11, sticky = "we", padx = 5, pady = 5)

        #Client 10 field
        notes_client10 = StringVar()
        notes_client10_selection = Entry(wrapper2frame, textvariable = notes_client10, width = 12)
        notes_client10_selection.grid(column = 9, row = 12, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 12, sticky = "we", padx = 5, pady = 5)

        #Client 11 field
        notes_client11 = StringVar()
        notes_client11_selection = Entry(wrapper2frame, textvariable = notes_client11, width = 12)
        notes_client11_selection.grid(column = 9, row = 13, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 13, sticky = "we", padx = 5, pady = 5)

        #Client 12 field
        notes_client12 = StringVar()
        notes_client12_selection = Entry(wrapper2frame, textvariable = notes_client12, width = 12)
        notes_client12_selection.grid(column = 9, row = 14, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 14, sticky = "we", padx = 5, pady = 5)

        #Client 13 field
        notes_client13 = StringVar()
        notes_client13_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client13_selection.grid(column = 9, row = 15, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 15, sticky = "we", padx = 5, pady = 5)

        #Client 14 field
        notes_client14 = StringVar()
        notes_client14_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client14_selection.grid(column = 9, row = 16, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 16, sticky = "we", padx = 5, pady = 5)

        #Client 15 field
        notes_client15 = StringVar()
        notes_client15_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client15_selection.grid(column = 9, row = 17, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 17, sticky = "we", padx = 5, pady = 5)

        #Client 16 field
        notes_client16 = StringVar()
        notes_client16_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client16_selection.grid(column = 9, row = 18, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 18, sticky = "we", padx = 5, pady = 5)

        #Client 17 field
        notes_client17 = StringVar()
        notes_client17_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client17_selection.grid(column = 9, row = 19, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 19, sticky = "we", padx = 5, pady = 5)

        #Client 18 field
        notes_client18 = StringVar()
        notes_client18_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client18_selection.grid(column = 9, row = 20, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 20, sticky = "we", padx = 5, pady = 5)

        #Client 19 field
        notes_client19 = StringVar()
        notes_client19_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client19_selection.grid(column = 9, row = 21, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 21, sticky = "we", padx = 5, pady = 5)

        #Client 20 field
        notes_client20 = StringVar()
        notes_client20_selection = Entry(wrapper2frame, textvariable = notes_client13, width = 12)
        notes_client20_selection.grid(column = 9, row = 22, columnspan = 1)

        notes_client1_notes = Button(wrapper2frame, image = notes_icon_resize)
        notes_client1_notes.grid(column = 10, row = 22, sticky = "we", padx = 5, pady = 5)

        #Table showing hours
        tabControl = ttk.Notebook(self) 
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


class ManagerPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Manager Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        


app = MainPage()
app.geometry("1280x720")
app.mainloop()