from math import e,pi
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
i = 1j
T = 4
def f(t):
    #return e**(pi*i*t)+1
    flag = int(t*2/T)%2
    if flag:
        return e**(4*pi/T*i*t)-1+i/2
    else:
        return e**(-4*pi/T*i*(t+T/4))+1+i/2


class Animate:
    def __init__(self):
        self.fig,self.ax = plt.subplots()
        self.xdata = []
        self.ydata = []
        self.line, = self.ax.plot([], [], 'b-', animated=False)
        self.text = self.ax.text(0.05,0.9,"",transform = self.ax.transAxes)

    def init(self):
        # 改变坐标轴及原点显示位置
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.spines['left'].set_position(('data', 0))

        # ax.text(0, 0, u'a大小不变 始终与v垂直')
        self.ax.axis('equal')
        lim = 3
        self.ax.set_xlim(-lim, lim)
        self.ax.set_ylim(-lim, lim)
        return self.line,

    def update(self,t):
        x,y = f(t).real,f(t).imag
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)
        self.text.set_text(str(t))

        return self.line,self.text
if __name__ == '__main__':
    model = Animate()
    ani = FuncAnimation(model.fig, model.update, frames=np.arange(0,10,0.01), init_func=model.init, blit=True, interval=10,repeat=True)
    plt.show()