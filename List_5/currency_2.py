from tkinter import *
import tkinter.ttk as ttk
import os
import pandas as pd
from datetime import datetime, timedelta
import threading

class Currency:
    def __init__(self):
        self.root = Tk()
        self.up_var = StringVar()
        self.data = self.get_data()
        self.cb_value1 = StringVar()
        self.cb_value2 = StringVar()
        self.output_value = StringVar()


        #compile program
        self.compile()



    def get_data(self):
        if os.path.isfile('data/data.csv'):
            data = pd.read_csv('data/data.csv')
            self.last_update = datetime.strptime(data['last_update'].iloc[0], "%H:%M %d/%m/%y")
            self.conn = True
        else:
            data = pd.DataFrame()
            self.last_update = None
        if len(data)==0 or self.last_update + timedelta(minutes=1) < datetime.now():
            try:
                data = pd.read_json('http://api.nbp.pl/api/exchangerates/tables/c/')
                data = pd.DataFrame(data.iloc[0]['rates'])
                self.last_update = datetime.now().strftime("%H:%M %d/%m/%y")
                data['last_update'] = self.last_update
                if not os.path.isdir("data"):
                    os.mkdir("data")
                data.to_csv("data/data.csv")
                self.connection(lost=False)

            except:
                self.connection()
        return data








    def connection(self, lost=True):
        self.up_var.set("Data has been updated!")
        con_lbl = Label(self.root, text="Connection lost", fg="red")
        con_sc = Label(self.root, textvariable=self.up_var, fg="green")
        if lost:
            con_lbl.place(x=0, y=0)
            self.conn = False
        elif lost is None:
            self.up_var.set("")
        elif not lost:
            con_sc.place(relx=1.0 ,x=0, y=25, anchor=NE)
            con_lbl.place_forget()
            self.conn=True



    def on_select_changed(self, event):
        if len(self.inp_value.get()) > 0 :
            self.update_result()



    def compile(self):
        self.root.title("Currency prices")
        self.root.geometry('650x250+0+0')
        lbl = Label(self.root, text="Cantor NBP")
        lbl.pack(side=TOP)
        up_lbl = Label(self.root, text=f"Last update: {self.data['last_update'].iloc[0]}")
        up_lbl.place(relx=1.0 , x=0, y=5, anchor=NE)

        #source currency
        values = list(self.data['code'])
        values.insert(0, "PLN")
        values = tuple(values)

        source_curr = Label(self.root, text="Provide source currency:")
        source_curr.place(relx=0.35 , rely=0.55, x=-39, y=-29, anchor=SE)
        cb1 = ttk.Combobox(self.root, textvariable = self.cb_value1)
        cb1.place(relx=0.35, rely=0.55, x=0, y=0, anchor=SE)
        cb1['values'] = values

        cb1.current(0)

        #targeted currency

        target_curr = Label(self.root, text="Provide target currency:")
        target_curr.place(relx=0.7, rely=0.55, x=-42, y=-29, anchor=SE)
        cb2 = ttk.Combobox(self.root, textvariable=self.cb_value2)
        cb2.place(relx=0.7, rely=0.55, x=0, y=0, anchor=SE)
        values = list(values)
        values[0], values[1] = values[1], values[0]
        values = tuple(values)
        cb2['values'] = values

        cb2.current(0)

        #Value_input
        inp_lab = Label(self.root, text="Amount:")
        inp_lab.place(relx=0.95, rely=0.55, x=-85, y=-29,anchor=SE)
        self.inp_value = StringVar()
        inp = Entry(self.root, textvariable = self.inp_value, width=15)
        inp.place(relx=0.95, rely=0.55, x=0, y=0, anchor=SE)

        #Count button
        ct_bt = Button(self.root, text="Count", width=16, command=self.update_result)
        ct_bt.place(relx=0.95, rely=0.55, x=0, y=40, anchor=SE)


        #Output
        output = Label(self.root, textvariable = self.output_value)
        output.place(relx=0.02, rely=0.85, x=0, y=0, anchor=W)


        #Exit button
        ex_bt = Button(self.root, text="Exit", command=quit, width=6)
        ex_bt.place(relx=1.0, rely=0.85, x=-90, y=0, anchor=W)



        #Hide_updated
        self.root.after(5000, self.connection, None)

        #Run program
        self.root.mainloop()



    def update_result(self, *args):
        try:
            if "," in self.inp_value.get():
                amount = self.inp_value.get()
                amount = amount.replace(",", ".")
                amount = float(amount)

            else:
                amount = float(self.inp_value.get())
            if self.cb_value1.get() == self.cb_value2.get():
                self.output_value.set("Choose different currencies")
                return
            if self.cb_value1.get() != "PLN":
                in_pln = amount * self.data[self.data['code']==self.cb_value1.get()]['bid'].iloc[0]
            else:
                in_pln = amount

            if self.cb_value2.get() != "PLN":
               result = in_pln / self.data[self.data['code'] == self.cb_value2.get()]['ask'].iloc[0]
            else:
                result = in_pln
            self.output_value.set(f"{self.inp_value.get()} {self.cb_value1.get()}  is worth {result:.2f} {self.cb_value2.get()}")
            # output.configure(text=f"{self.inp_value.get()} {self.cb_value1.get()} is worth {result}")
        except:
            if len(self.inp_value.get()) == 0:
                self.output_value.set("Provide amount of currency")
            else:
                self.output_value.set("Dane są w złym formacie")


    def quit(self):
        import sys
        sys.exit()


if __name__ == '__main__':
    Currency()

