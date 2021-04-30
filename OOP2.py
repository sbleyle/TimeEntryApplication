# A class is a blueprint that is used to make objects. An object is an instance of the class.
# Instance variables?
from tkinter import *

class App():
    #Fields - Attributes
    #Constructors - Special methods called when we first create an instance
    def __init__(self):
        #Build my GUI (all my instance variables)

        self.root = Tk() #Capitalize methods are constructors

        self.frame = Frame(self.root, padx = 20, pady = 20, bg = "#4E4187")
        self.label1 = Label(self.frame, text = "Enter First name", bg = "#4E4187", width = 30, height = 1, fg = "#7DDE92")
        self.label2 = Label(self.frame, text = "Enter Last name", bg = "#4E4187", width = 30, height = 1, fg = "#7DDE92")
        self.label3 = Label(self.frame, text = "Enter Access Code", bg = "#4E4187", width = 30, height = 1, fg = "#7DDE92")

        self.text1 = Text(self.frame, width = 30, height = 1, borderwidth = 2, relief = GROOVE, fg = "#7DDE92")
        self.text2 = Text(self.frame, width = 30, height = 1, borderwidth = 2, relief = GROOVE, fg = "#7DDE92")
        self.text3 = Text(self.frame, width = 30, height = 1, borderwidth = 2, relief = GROOVE, fg = "#7DDE92")
        
        self.button1 = Button(self.frame, text = "Login")

        self.label1.grid(row = 0, column = 0)
        self.label2.grid(row = 1, column = 0)
        self.label3.grid(row = 2, column = 0)

        self.text1.grid(row = 0, column = 1, columnspan = 2)
        self.text2.grid(row = 1, column = 1, columnspan = 2)
        self.text3.grid(row = 2, column = 1, columnspan = 2)

        self.button1.grid(row = 3, column = 1, sticky = "NSEW")

        self.frame.pack()
        self.root.mainloop()
    #Method - Behaviours

a = App() #Create an app object and store the reference in a