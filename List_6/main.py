import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
from tkinter import *
from sympy import *
from sympy.parsing.sympy_parser import standard_transformations, parse_expr, implicit_multiplication_application
from sympy.utilities.lambdify import lambdify
import re
"""

Created for university project.
@author: Kacper Rownicki
"""



class MathManager:
    """Class that represents the whole porogram.


    """
    def __init__(self, master):
        """
        Initialization of buttons, variables, entries, texts etc.


        :param master: Tkinter master
        """

        #TextVariables
        self.func = StringVar()


        self.xstart = DoubleVar()
        self.xend = DoubleVar()
        self.ystart = DoubleVar()
        self.yend = DoubleVar()
        self.xstart.set(-10)
        self.xend.set(10)
        self.ystart.set(-10)
        self.yend.set(10)

        self.title = StringVar()

        self.xLabel = StringVar()

        self.yLabel = StringVar()

        self.iLegend = IntVar()
        self.first_plot=True
        self.err_flag = False


        #Labels
        self.lbl1 = Label(master, text="Podaj funkcje:")
        self.lbl1.place(relx=0.1, rely=0.2, x=0, y=0)

        #Plot config
        self.config_plot = Label(master, text="Skonfiguruj wykres:")
        self.config_plot.place(relx=0.1, rely=0.2, x=0, y=200)

        self.x_lbl = Label(master, text="X: ")
        self.x_lbl.place(relx=0.1, rely=0.2, x=0, y=230)

        self.x_start_lbl = Label(master, text="OD")
        self.x_start_lbl.place(relx=0.1, rely=0.2, x=30, y=230)
        self.x_end_lbl = Label(master, text="DO")
        self.x_end_lbl.place(relx=0.1, rely=0.2, x=150, y=230)

        self.y_lbl = Label(master, text="Y: ")
        self.y_lbl.place(relx=0.1, rely=0.2, x=0, y=271)

        self.y_start_lbl = Label(master, text="OD")
        self.y_start_lbl.place(relx=0.1, rely=0.2, x=30, y=271)
        self.y_end_lbl = Label(master, text="DO")
        self.y_end_lbl.place(relx=0.1, rely=0.2, x=150, y=271)

        self.tit_lbl = Label(master, text="Tytuł wykresu:")
        self.tit_lbl.place(relx=0.1, rely=0.2, x=0, y=312)

        self.xlab = Label(master, text="Etykieta X:")
        self.xlab.place(relx=0.1, rely=0.2, x=0, y=343)


        self.ylab = Label(master, text="Etykieta Y:")
        self.ylab.place(relx=0.1, rely=0.2, x=0, y=374)

        self.start_plot = Button(master, text="Rysuj", command=lambda: self.process(master), width=13)
        self.start_plot.place(relx=0.1, rely=0.2, x=252, y=420)




        #Inputs
        self.func_inp = Entry(master, textvariable=self.func)
        self.func_inp.place(relx=0.1, rely=0.2, x=0, y=20, width=350)
        self.func_inp.focus_set()

        #Plot_inputs
        self.xrng_start = Entry(master, textvariable=self.xstart)
        self.xrng_start.place(relx=0.1, rely=0.2, x=75, y=227, width=60)


        self.xrng_end = Entry(master, textvariable=self.xend)
        self.xrng_end.place(relx=0.1, rely=0.2, x=194, y=227, width=60)

        self.yrng_start = Entry(master, textvariable=self.ystart)
        self.yrng_start.place(relx=0.1, rely=0.2, x=75, y=268, width=60)

        self.yrng_end = Entry(master, textvariable=self.yend)
        self.yrng_end.place(relx=0.1, rely=0.2, x=194, y=268, width=60)

        self.title_inp = Entry(master, textvariable=self.title, width=28)
        self.title_inp.place(relx=0.1, rely=0.2, x=110, y=308)

        self.xlab_inp = Entry(master, textvariable=self.xLabel, width=28)
        self.xlab_inp.place(relx=0.1, rely=0.2, x=110, y=339)

        self.ylab_inp = Entry(master, textvariable=self.yLabel, width=28)
        self.ylab_inp.place(relx=0.1, rely=0.2, x=110, y=370)

        self.legend_but = Checkbutton(master, text="Legenda", variable=self.iLegend)
        self.legend_but.place(relx=0.1, rely=0.2, x=0, y=420)

        #Buttons
        self.buttC = Button(master, text="C", command=self.clear)
        self.buttC.place(relx=0.1, rely=0.2, x=0, y=70, width=35)

        self.buttCE = Button(master, text="CE", command=self.backspace)
        self.buttCE.place(relx=0.1, rely=0.2, x=35, y=70, width=35)

        self.buttPlus = Button(master, text=u"\u002b", command=lambda: self.add_element("+"))
        self.buttPlus.place(relx=0.1, rely=0.2, x=70, y=70, width=35)

        self.buttMinus = Button(master, text=u"\u2212", command=lambda: self.add_element("-"))
        self.buttMinus.place(relx=0.1, rely=0.2, x=105, y=70, width=35)

        self.buttMulti = Button(master, text=u"\u00d7", command=lambda: self.add_element("*"))
        self.buttMulti.place(relx=0.1, rely=0.2, x=140, y=70, width=35)

        self.buttDiv = Button(master, text=u"\u00f7", command=lambda: self.add_element("/"))
        self.buttDiv.place(relx=0.1, rely=0.2, x=175, y=70, width=35)

        self.buttSin = Button(master, text="sin", command=lambda: self.add_element("sin()"))
        self.buttSin.place(relx=0.1, rely=0.2, x=210, y=70, width=35)

        self.buttCos = Button(master, text="cos", command=lambda: self.add_element("cos()"))
        self.buttCos.place(relx=0.1, rely=0.2, x=245, y=70, width=35)

        self.buttTg = Button(master, text="tg", command=lambda: self.add_element("tg()"))
        self.buttTg.place(relx=0.1, rely=0.2, x=280, y=70, width=35)

        self.buttEl = Button(master, text="e", command=lambda: self.add_element("e"))
        self.buttEl.place(relx=0.1, rely=0.2, x=315, y=70, width=35)




        self.butt1 = Button(master, text="1", command=lambda: self.add_element("1"))
        self.butt1.place(relx=0.1, rely=0.2, x=0, y=100, width=35)

        self.butt2 = Button(master, text="2", command=lambda: self.add_element("2"))
        self.butt2.place(relx=0.1, rely=0.2, x=35, y=100, width=35)

        self.butt3 = Button(master, text="3", command=lambda: self.add_element("3"))
        self.butt3.place(relx=0.1, rely=0.2, x=70, y=100, width=35)

        self.butt4 = Button(master, text="4", command=lambda: self.add_element("4"))
        self.butt4.place(relx=0.1, rely=0.2, x=105, y=100, width=35)

        self.butt5 = Button(master, text="5", command=lambda: self.add_element("5"))
        self.butt5.place(relx=0.1, rely=0.2, x=140, y=100, width=35)

        self.butt6 = Button(master, text="6", command=lambda: self.add_element("6"))
        self.butt6.place(relx=0.1, rely=0.2, x=175, y=100, width=35)

        self.butt7 = Button(master, text="7", command=lambda: self.add_element("7"))
        self.butt7.place(relx=0.1, rely=0.2, x=210, y=100, width=35)

        self.butt8 = Button(master, text="8", command=lambda: self.add_element("8"))
        self.butt8.place(relx=0.1, rely=0.2, x=245, y=100, width=35)

        self.butt9 = Button(master, text="9", command=lambda: self.add_element("9"))
        self.butt9.place(relx=0.1, rely=0.2, x=280, y=100, width=35)
        self.butt0 = Button(master, text = "0", command=lambda: self.add_element("0"))
        self.butt0.place(relx=0.1, rely=0.2, x=315, y=100, width=30)

        self.buttSq = Button(master, text=u"a\u00b2", command=lambda: self.add_element("^2") )
        self.buttSq.place(relx=0.1, rely=0.2, x=0, y=130, width=35)

        self.buttCb = Button(master, text=u"a\u00b3", command=lambda: self.add_element("^3"))
        self.buttCb.place(relx=0.1, rely=0.2, x=35, y=130, width=35)

        self.buttToN = Button(master, text=u"a\u207f", command=lambda: self.add_element("^"))
        self.buttToN.place(relx=0.1, rely=0.2, x=70, y=130, width=35)

        self.buttSRoot = Button(master, text=u"\u221a", command=lambda: self.add_element("sqrt()"))
        self.buttSRoot.place(relx=0.1, rely=0.2, x=105, y=130, width=35)

        self.buttCRoot = Button(master, text=u"\u221b", command=lambda: self.add_element("cbrt()"))
        self.buttCRoot.place(relx=0.1, rely=0.2, x=140, y=130, width=35)

        self.buttX = Button(master, text="x", command=lambda: self.add_element("x"))
        self.buttX.place(relx=0.1, rely=0.2, x=175, y=130, width=35)

        self.buttXX = Button(master, text=u"x\u00b2", command=lambda: self.add_element("x^2"))
        self.buttXX.place(relx=0.1, rely=0.2, x=210, y=130, width=35)

        self.buttLn = Button(master, text=u"\u33d1", command=lambda: self.add_element("ln()"))
        self.buttLn.place(relx=0.1, rely=0.2, x=245, y=130, width=35)

        self.buttLog = Button(master, text=u"\u33d2",command=lambda: self.add_element("log()"))
        self.buttLog.place(relx=0.1, rely=0.2, x=280, y=130, width=35)

        self.buttPi = Button(master, text=u"\u03c0", command=lambda: self.add_element(u"\u03c0"))
        self.buttPi.place(relx=0.1, rely=0.2, x=315, y=130, width=35)

        #Plot blank
        self.plot(master)

        #Quit button
        self.exButt = Button(master, text="Koniec", command=self.quit)
        self.exButt.place(relx=0.8, rely=0.2, x=0, y=420, width=120)







    def process(self, master):
        """
        Processing the function input - converting string into sympy format and then numpy to perform numerical calculations.
        Then ploting the functions.

        :param master:Tkinter
        :return:
        """

        if len(self.func.get()) == 0: return
        self.working_func = self.func.get()
        self.working_func = self.working_func.replace("^", "**")
        self.working_func = self.working_func.replace(u"\u03c0", "pi")
        patt = re.compile(r'(\d)(pi)')
        self.working_func = patt.sub(r"\1*\2", self.working_func)
        self.working_func = self.working_func.replace(",",".")
        self.list_func = self.working_func.split(";")

        if len(self.list_func[-1]) == 0:
            self.list_func.pop()

        transformations = (standard_transformations + (implicit_multiplication_application,))
        x = Symbol('x')
        try:
            for func in range(len(self.list_func)):
                if 'x' in self.list_func[func]:
                    self.list_func[func] = lambdify(x, parse_expr(self.list_func[func], transformations=transformations),'numpy')
                else:
                    self.list_func[func] = float(N(self.list_func[func]))


        except:
            self.value_err(master)
            return

        self.arg = np.linspace(self.xstart.get(), self.xend.get(), 1000)
        self.values = []
        try:
            for f in self.list_func:
                if type(f) != float:
                    self.values.append(f(self.arg))
                else:
                    self.values.append(np.ones(1000)*f)
        except:
            self.value_err(master)
            return
        # self.values = [f(self.arg) for f in self.list_func]
        self.first_plot = False
        self.plot(master)




    def plot(self, master):
        """
        Ploting the functions or create first blank plot.

        :param master: Tkinter master
        :return:
        """
        f = Figure(figsize=(4,4), dpi=100)
        a = f.add_subplot(111, xlim=(self.xstart.get(), self.xend.get()), ylim=(self.ystart.get(), self.yend.get()),
                          title=self.title.get())
        canvas = FigureCanvasTkAgg(f, master)

        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=-10, relx=0.97, rely=0.1, anchor=NE)

        if self.first_plot:

            a.grid()
            a.plot()
            toolbar = NavigationToolbar2Tk(canvas, master)
            toolbar.update()
            canvas._tkcanvas.place(x=0, y=0, relx=0.97, rely=0.1, anchor=NE)
            f.tight_layout()
        else:
            f.delaxes(a)
            a = f.add_subplot(111, xlim=(self.xstart.get(), self.xend.get()), ylim=(self.ystart.get(), self.yend.get()),
                          title=self.title.get(), xlabel=self.xLabel.get(), ylabel=self.yLabel.get())
            f.tight_layout()
            for i in range(len(self.list_func)):
                a.plot(self.arg, self.values[i], label=self.func.get().split(";")[i])
            a.grid()
        if self.iLegend.get()==1:
            a.legend()
        self.value_err(master, False)









    def add_element(self, element):
        """
        Adding element to Entry field of funtions.
        Needed for buttons below the Entry field.

        :param element:
        :return:
        """
        self.func_inp.insert(INSERT,element)
        if element in ["sin()", "cos()", "tg()", "sqrt()", "cbrt()"]:
            self.func_inp.icursor(self.func_inp.index(INSERT)-1)

    def backspace(self):
        """
        Removing last element in the Entry field(function)
        (Backspace button)

        :return:
        """
        self.func_inp.delete(first=self.func_inp.index(INSERT)-1)

    def clear(self):
        """
        Removing whole content in Entry field(function)

        :return:
        """
        self.func_inp.delete(0, END)
    def value_err(self, master, error=True):
        """
        Handling the error when value in input function is incorrect.
        :param master:
        :param error:
        :return:
        """
        if error and not self.err_flag:
            self.errLab = Label(master, text="Błędnie podana wartość.", fg='red')
            self.errLab.place(relx=0.1, rely=0.15, x=-90, y=0, width=350)
            self.err_flag = True
        elif not error and self.err_flag:
            self.errLab.destroy()
            self.err_flag = False


    def quit(self):
        """
        Exit the program.

        :return:
        """
        import sys; sys.exit()


if __name__ == "__main__":
    root = Tk()
    root.title("MathManager")
    root.geometry('1000x600+0+0')
    ex = MathManager(root)
    root.mainloop()
