import numpy as np
import argparse
from scipy.integrate import odeint
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Program służy do generowania wykresów: x(t), v(t) i v(x) w wahadle tłumionym z okresową siłą wymuszającą.')
parser.add_argument('spec', metavar='args', nargs=5, help="")






def f(y, r, Q, w, A):
    th, v = y[0], y[1]

    dth = v
    dp = -(1 / Q) * v - np.sin(th) + A * np.cos(w * r)

    return [dth, dp]
r = np.linspace(0, 20, 4000)


args = []
for x in parser.parse_args().spec:
    try:
        args.append(float(x))
    except ValueError:
        num1, num2 = x.split("/")
        args.append(float(num1)/float(num2))



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

print(args)
