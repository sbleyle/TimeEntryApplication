from tkinter import *

class Win1:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x44")
        self.frame = Frame(self.master)
        self.show_widgets()

    def show_widgets(self):
        self.frame = Frame(self.master)
        self.master.title("Window n.1")
        self.create_button("Click to open Window 2", Win2)
        self.create_button("Click to open Window 3", Win3)
        self.frame.pack()

    def create_button(self, text, _class):
        Button(self.frame, text = text, command = lambda: self.new_window(_class)).pack()

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

class Win2(Win1):

    def show_widgets(self):
        self.master.title("Window 2")
        self.frame = Frame(self.master, bg = "red")
        self.quit_button = Button(self.frame, text = f"Quit window 3 from window 2", command = self.close_window)
        self.frame.pack()
        self.quit_button.pack()
        self.create_button("Open window 3 from window 2", Win3)
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
app = Win1(root)
root.mainloop()