import tkinter as tk
from tkinter import ttk
import backend

LARGE_FONT= ("Verdana", 12)



       

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="organizer_calendar_clock_pencil_10047.ico")
        tk.Tk.wm_title(self, "Sea of BTC client")
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, BTCe_Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=("""ALPHA Bitcoin trading application
        use at your own risk. There is no promise
        of warranty."""), font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_frame(BTCe_Page))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=quit)
        button2.pack()



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Client field
        engagement_label = ttk.Label(self, text = "Client", width = 40)
        engagement_label.grid(column = 0, row = 1, columnspan = 4, sticky = "w", padx = 5)
        
        selected_client = tk.StringVar()
        client1 = ttk.Combobox(self, textvariable = selected_client, state = 'readonly')
        client1['values'] = backend.client_dropdown()
        client1.grid(column = 0, row = 2, columnspan = 4, sticky = "we", padx = 5)
        client1.get()

        #Engagement field
        engagement_label = ttk.Label(self, text = "Engagement", width = 50)
        engagement_label.grid(column = 0, row = 3, columnspan = 5, sticky = "w", padx = 5)
        
        selected_engagement = tk.StringVar()
        engagement1 = ttk.Combobox(self, textvariable = selected_engagement, state = 'readonly', postcommand = lambda: engagement1.configure(value = backend.engagement_dropdown(client1.get())))
        engagement1['values'] = backend.engagement_dropdown(client1.get())
        engagement1.grid(column = 0, row = 4, columnspan = 5, sticky = "we", padx = 5)

        #Engagement Code field
        engagementcode_label = ttk.Label(self, text = "Engagement Code", width = 40)
        engagementcode_label.grid(column = 0, row = 5, columnspan = 4, sticky = "w", padx = 5)
        
        selected_code = tk.StringVar()
        code1 = ttk.Combobox(self, textvariable = selected_code, state = 'readonly', postcommand = lambda: code1.configure(value = backend.engagementcode_dropdown(client1.get(), engagement1.get())))
        code1['values'] = backend.client_dropdown()
        code1.grid(column = 0, row = 6, columnspan = 4, sticky = "we", padx = 5)
        code1.get()

        select_button = ttk.Button(self, text = "Select")
        select_button.pack()
        #select_button.grid(column = 0, row = 7, padx = 5, pady = 5)
        #label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)

        #button1 = ttk.Button(self, text="Back to Home",
                            #command=lambda: controller.show_frame(StartPage))
        #button1.pack()


class BTCe_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        #label.pack(pady=10,padx=10)

        #button1 = ttk.Button(self, text="Back to Home",
                            #command=lambda: controller.show_frame(StartPage))
        #button1.pack()

        #Client field
        client_label = ttk.Label(self, text = "Client", width = 40)
        client_label.pack()
        #client_label.grid(column = 0, row = 1, columnspan = 4, sticky = "w", padx = 5)
        
        selected_client = tk.StringVar()
        client1 = ttk.Combobox(self, textvariable = selected_client, state = 'readonly')
        client1['values'] = backend.client_dropdown()
        client1.pack()
        #client1.grid(column = 0, row = 2, columnspan = 4, sticky = "we", padx = 5)
        client1.get()

        #Engagement field
        engagement_label = ttk.Label(self, text = "Engagement", width = 50)
        engagement_label.pack()
        #engagement_label.grid(column = 0, row = 3, columnspan = 5, sticky = "w", padx = 5)
        
        selected_engagement = tk.StringVar()
        engagement1 = ttk.Combobox(self, textvariable = selected_engagement, state = 'readonly', postcommand = lambda: engagement1.configure(value = backend.engagement_dropdown(client1.get())))
        engagement1['values'] = backend.engagement_dropdown(client1.get())
        engagement1.pack()
        #engagement1.grid(column = 0, row = 4, columnspan = 5, sticky = "we", padx = 5)

        #Engagement Code field
        engagementcode_label = ttk.Label(self, text = "Engagement Code", width = 40)
        engagementcode_label.pack()
        #engagementcode_label.grid(column = 0, row = 5, columnspan = 4, sticky = "w", padx = 5)
        
        selected_code = tk.StringVar()
        code1 = ttk.Combobox(self, textvariable = selected_code, state = 'readonly', postcommand = lambda: code1.configure(value = backend.engagementcode_dropdown(client1.get(), engagement1.get())))
        code1['values'] = backend.client_dropdown()
        code1.pack()
        #code1.grid(column = 0, row = 6, columnspan = 4, sticky = "we", padx = 5)
        code1.get()

        select_button = ttk.Button(self, text = "Select", command = lambda: controller.show_frame(StartPage))
        select_button.pack()
        #select_button.grid(column = 0, row = 7, padx = 5, pady = 5)

app = SeaofBTCapp()
app.geometry("1280x720")
app.mainloop()