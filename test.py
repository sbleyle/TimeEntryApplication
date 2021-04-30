from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Codemy.com - Learn To Code!')
root.geometry("400x400")


class TimeEntryApp:
    def __init__(self, master):
        myframe = Frame(master)
        myframe.pack()

        self.mybutton = Button(master, text = "Click Me!", command = self.clicker)
        self.mybutton.pack(pady = 20)

    def clicker(self):
        print("It worked!")


TEA = TimeEntryApp(root)


root.mainloop()