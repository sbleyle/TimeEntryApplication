from tkinter import *
import forecast

class Frames(object):

    def __init__(self):
        pass

    def main_frame(self, root):
        root.title('WeatherMe')
        root.geometry('300x100')

        self.query = StringVar()

        Label(root, text='Enter a city below').pack()

        Entry(root, textvariable=self.query).pack()

        Button(root, text="Submit", command=self.result_frame).pack()

    def result_frame(self):
        result = Toplevel()
        result.title('City')
        result.geometry('1600x150')

        #print(self.query.get()) #This would print the StringVar's value , use this in whatever way you want.
        
        city = Entry(result).pack()

        Ans = self.query.get()
        print(Ans)
        city.insert(0, Ans)

        #Entry(result, textvariable = self.query.get()).pack()

        Button(result, text="OK", command=result.destroy).pack()

root = Tk()
app = Frames()
app.main_frame(root)
root.mainloop()