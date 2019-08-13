import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

i = 1j
T = 4   #此处设定初始值 后更改成与js相符
deltat = 0.01
points = [] #给定数据集中的点
length = 0  #点的个数 由此确定ft的映射
xmax = xmin = ymax = ymin = 0
def readData(path):
    global points,length,T,deltat,xmax , xmin , ymax , ymin
    with open(path,'r') as data:
        info = data.readline().split()
        T, deltat = info
        T,deltat = float(T),float(deltat)
        info = data.readline().split()
        while info:
            x,y = info
            points.append([float(x),float(y)])
            info = data.readline().split()

    length = len(points)
    points = np.array(points)
    X, Y = points[:,0],points[:,1]
    points = points - [np.median(X), np.median(Y)]  #重心移动至原点附近 画图好看
    X, Y = points[:, 0], points[:, 1]#重新获取数据求最值
    xmax = max(X)
    xmin = min(X)
    ymax = max(Y)
    ymin = min(Y)

'''
def f(t):   #调试函数 需取消动画中关于points的部分
    #return e**(pi*i*t)+1
    flag = int(t*2/T)%2
    if flag:
        return e**(4*pi/T*i*t)-1+i/2
    else:
        return e**(-4*pi/T*i*(t+T/4))+1+i/2
'''
def f(t):   #点的位置随时间变化(给定)
    index = int(round(length * (t%T) / T))
    return points[index][0]+points[index][1]*i



class Animate:  #动画效果
    def __init__(self):
        spanx = xmax - xmin
        spany = ymax - ymin
        #因为要画圆所以必须xy轴单位长度比例为1 而数据集中xy的范围不确定 故需要放缩画布
        self.fig,self.ax = plt.subplots(figsize=(10*spanx/(spanx+spany), 10*spany/(spanx+spany)))
        self.xdata = []
        self.ydata = []
        self.line, = self.ax.plot([], [], color = 'cyan',linestyle = '-')

    def init(self):
        # 改变坐标轴及原点显示位置
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.spines['left'].set_position(('data', 0))

        self.ax.axis('off')
        self.ax.axis('equal')

        scale = 1.5

        self.ax.set_xlim(xmin*scale, xmax*scale)
        self.ax.set_ylim(ymin*scale, ymax*scale)

        return self.line,   #单个返回值一定要加逗号 变成turple

    def update(self,t):
        x,y = f(t).real,f(t).imag
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)

        return self.line,

svgPath = 'data.svg'
os.system('node svgToft.js' + ' ' + svgPath)    #利用js处理svg数据
ftPath = 'ft.txt'
readData(ftPath)  #此处文件名应与js保存的文件吻合
if __name__ == '__main__':

    #os.system('del' + ' ' + ftPath) #在readData后删会出现问题

    plt.style.use('dark_background')
    model = Animate()
    ani = FuncAnimation(model.fig, model.update, frames=np.arange(0, 2*T, deltat), init_func=model.init, blit=True, interval=20, repeat=False)
    #ani.save('sample4.gif', writer='pillow')

    plt.show()