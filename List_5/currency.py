from tkinter import *
import tkinter.ttk as ttk
import os
import pandas as pd
from datetime import datetime, timedelta
import tkinter.messagebox as msb


class Currency():
    def __init__(self):
        self.root = Tk()
        self.data = self.get_data()
        self.cb_value = StringVar()

        self.compile()


    def get_data(self):
        if os.path.isfile('data/data.csv'):
            data = pd.read_csv('data/data.csv')
            last_update = datetime.strptime(data['last_update'].iloc[0], "%H:%M %d/%m/%y")
        else:
            data = pd.DataFrame()
            last_update = None
        if len(data)==0 or last_update + timedelta(minutes=15) < datetime.now():
            try:
                data = pd.read_json('http://api.nbp.pl/api/exchangerates/tables/c/')
                data = pd.DataFrame(data.iloc[0]['rates'])
                last_update = datetime.now().strftime("%H:%M %d/%m/%y")
                data['last_update'] = last_update
                if not os.path.isdir("data"):
                    os.mkdir("data")
                data.to_csv("data/data.csv")
                print("Udało się zaktualizować dane")
            except:
                print("Brak internetu")
        return data



    def combobox(self, window):

        cb = ttk.Combobox(window, textvariable = self.cb_value)
        cb.place(x = 0, y = 0)
        cb['values'] = ("USD", "PLN", "CAD", "EUR")
        cb.current(0)
        cb.bind("<<ComboboxSelected>>", self.on_select_changed)

    def on_select_changed(self, event):
        msb.showinfo("Info", self.cb_value.get())





    def compile(self):
        self.root.title("Currency prices")
        self.root.geometry('600x500+0+0')
        lbl = Label(self.root, text="Poznaj ceny walut!")
        lbl.pack(side=TOP)
        self.combobox(self.root)




        self.root.mainloop()



if __name__ == '__main__':
    Currency()

    # root = Tk()
    # root.mainloop()
