import numpy as np
import argparse
from scipy.integrate import odeint
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Program służy do generowania wykresów: x(t), v(t) i v(x) w wahadle tłumionym z okresową siłą wymuszającą.')
parser.add_argument('-Q',  metavar="Q", nargs=1,
                    help="Pass Q argument")
parser.add_argument('-w',  metavar="w", nargs=1,
                    help="Pass w argument")
parser.add_argument('-A',  metavar="A", nargs=1,
                    help="Pass A argument")
parser.add_argument('-v',  metavar="v0", nargs=1,
                    help="Pass v0 argument")
parser.add_argument('-th',  metavar="th0", nargs=1,
                    help="Pass th0 argument")


def addFloat(x, lst):
    if x is None:
        raise ValueError("Every paramter should be passed")
    x = x[0]
    try:
        lst.append(float(x))
    except:
        num1, num2 = x.split("/")
        lst.append(float(num1) / float(num2))


def f(y, r, Q, w, A):
    th, v = y[0], y[1]

    dth = v
    dp = -(1 / Q) * v - np.sin(th) + A * np.cos(w * r)

    return [dth, dp]
r = np.linspace(0, 20, 4000)

pars = parser.parse_args()
args = []
addFloat(pars.Q, args)
addFloat(pars.w, args)
addFloat(pars.A, args)
addFloat(pars.v, args)
addFloat(pars.th, args)


y0 = [args[4], args[3]]

y1 = odeint(f, y0, r, args=(args[0], args[1], args[2]))
plt.subplot(1,2,1)
plt.plot(r, y1[:,0], label="x(t)")
plt.plot(r, y1[:,1], label="v(t)")
plt.legend(loc="upper right")
plt.subplot(1,2,2)
plt.plot(y1[:,0], y1[:,1], label="v(x)")
plt.legend(loc="upper right")

plt.show()


