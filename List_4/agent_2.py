import matplotlib.pyplot as plt
from matplotlib import animation
import time
import numpy as np
from agent import Agent

x = Agent(size=15, steps=300)
data = x.generate_data()

fig, ax = plt.subplots()
ax.set_xlim(-x.board_size,x.board_size)
ax.set_ylim(-x.board_size,x.board_size)
l, = ax.plot(0,0)
ax.grid()

def init():
    l.set_data(0,0)
def update(i):
    l.set_data(data[:i,0], data[:i,1])
#aby zmienić czas między nowymi liniami należy zmienić parametr "interval" w ms.

anim = animation.FuncAnimation(fig, update, init_func=init, frames=len(data),interval=300,  blit=False)

anim.save('animation_test_tj.gif', fps=20, writer="avconv", codec="libx264")

# Aby uzyskać format mp4 należy odkomentować linię poniżej
# anim.save('animation_test.mp4', fps=20, writer="avconv", codec="libx264")
# anim.to_html5_video()
plt.show()



#     # animate = lambda i: l.set_data(t[:i], x[:i])
# for i in range(len(data)):
#     animate(i)
#     time.sleep(0.05)
#     plt.show()
