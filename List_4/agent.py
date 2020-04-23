import matplotlib.pyplot as plt
from matplotlib import animation
import os
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


def init():
    ax.scatter(0,0)
def update(i):
    ax.cla()
    ax.set_xlim(-x.board_size, x.board_size)
    ax.set_ylim(-x.board_size, x.board_size)
    ax.grid()
    ax.scatter(data[i,0], data[i,1])
    plt.savefig(f"png{i}.png")

if __name__ == "__main__":
    x = Agent(size=15, steps=100)
    data = x.generate_data()
    try:
        os.mkdir("folder_png")
        os.chdir("folder_png")
    except:
        os.chdir("folder_png")
    fig, ax = plt.subplots()
    ax.set_xlim(-x.board_size,x.board_size)
    ax.set_ylim(-x.board_size,x.board_size)
    ax.grid()
    #aby zmienić szybość animacji należy zmienić parmetr interval
    anim = animation.FuncAnimation(fig, update, init_func=init, frames=len(data), interval=300,  blit=False)
    gif_path = os.path.join(os.path.dirname(os.getcwd()), "animation_test1.gif")
    anim.save(gif_path, fps=20, writer="avconv", codec="libx264")
    plt.show()


# Aby uzyskać format mp4 należy odkomentować linię poniżej
# anim.save('animation_test.mp4', fps=20, writer="avconv", codec="libx264")
# anim.to_html5_video()


