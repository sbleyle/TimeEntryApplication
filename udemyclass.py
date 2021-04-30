from tkinter import *
from tkinter import ttk


class HelloWorld(Tk):
    def __init__(self):
        super().__init__()

        self.title("Hello, world.")

        UserInputFrame(self).pack()

class UserInputFrame(Frame):
    def __init__(self, container):
        super().__init__(container)

        self.user_input = StringVar()

        label = Label(self, text = "Enter your name:")
        entry = Entry(self, textvariable = self.user_input)
        button = Button(self, text = "Enter", command = self.greet)

        label.pack(side = "left")
        entry.pack(side = "left")
        button.pack(side = "left")

    def greet(self):
        print(f"Hello, {self.user_input.get()}!")


root = HelloWorld()
root.mainloop()