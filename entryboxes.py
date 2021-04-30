from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Codemy.com - Learn To Code!')
root.geometry("700x500")

my_entries = []

def something():
    entry_list = ''

    for entries in my_entries:
        entry_list = entry_list + str(entries.get()) + '\n'
        my_label.config(text = entry_list)

    print(my_entries[0].get())

# Row loop
for y in range(5):
    # Column loop
    for x in range(5):
        my_entry = Entry(root)
        my_entry.grid(row = y, column = x)
        my_entries.append(my_entry)

my_button = Button(root, text = "Button", command = something)
my_button.grid(row = 6, column = 0, pady = 20)

my_label = Label(root, text = '')
my_label.grid(row = 7, column = 0, pady = 20)
root.mainloop()