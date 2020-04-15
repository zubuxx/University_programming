import matplotlib.pyplot as plt
from matplotlib import animation
import time
import numpy as np




class Agent():

    def __init__(self ,steps=1000, size=20):
        self.position = [0.0 ,0.0]
        self.steps = steps
        self.random_steps = None
        self.board_size = size
        self.line = None
        self.data = None
        self.z = []


    def move_agent(self, step):
        # ruch pierwszej współrzędnej
        out = False
        self.position[0] += step[0]
        if self.position[0] > self.board_size:
            out = True
            self.position[0] -= 2* self.board_size
        elif self.position[0] < -self.board_size:
            out = True
            self.position[0] += 2 * self.board_size
        # ruch drógiej współrzędnej
        self.position += step[1]
        if self.position[1] > self.board_size:
            out = True
            self.position[1] -= 2 * self.board_size
        elif self.position[1] < -self.board_size:
            out = True
            self.position[1] += 2 * self.board_size
        if out:
            self.z.append(np.array([np.nan, np.nan]))
        return np.array([self.position[0], self.position[1]])

    def generate_steps(self, n=1000):
        self.random_steps = np.random.randn(n, 2)

    def animation_frame(self, i):
        self.line.set_xdata(self.data[:i, 0])
        self.line.set_ydata(self.data[:i, 1])
        return self.line,

    def generate_data(self):
        if self.random_steps is None:
            self.generate_steps(self.steps)
        track = np.array([[0, 0]])
        for s in self.random_steps:
            i = self.move_agent(s)
            self.z.append(i)
        self.data = np.concatenate((track, self.z))
        return self.data

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

anim.save('animation_test.gif', fps=20, writer="avconv", codec="libx264")

# Aby uzyskać format mp4 należy odkomentować linię poniżej
# anim.save('animation_test.mp4', fps=20, writer="avconv", codec="libx264")
# anim.to_html5_video()
plt.show()



#     # animate = lambda i: l.set_data(t[:i], x[:i])
# for i in range(len(data)):
#     animate(i)
#     time.sleep(0.05)
#     plt.show()
