from math import e,pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

i = 1j
T = 4   #应与js相符 后续解决
deltat = 0.01
points = [] #给定数据集中的点
length = 0  #点的个数 由此确定ft的映射

def readData(path):
    global points,length,T,deltat
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

class Fn:
    N = 60  #箭头个数 越多拟合越精确
    def __init__(self,n):
        self.f = lambda t:e**(n*2*pi/T*i*t)    #此处n的传递很关键 类似闭包写法
        self.f0 = lambda t:e**(-n*2*pi/T*i*t)   #令自己不动的函数 求c
        self.c = 0          #常量系数
        self.r = 0          #改箭头轨迹的半径(圆心会变)

def F(t):   #点的位置随时间变化(由计算出的傅里叶级数拟合出)
    res = 0
    for fn in funclist:
        res += fn.c * fn.f(t)
    return res

def compute(funclist):  #计算系数c 从而得到Ft
    for fn in funclist:
        deltat = 0.01
        for t in np.arange(0,T,deltat):
            fn.c += f(t)*fn.f0(t)*deltat
        fn.c /= T   #此处为推广 周期不为1时不满足公式
        fn.r = abs(fn.c)
    return funclist

class Animate:  #动画效果
    def __init__(self,funclist):
        self.funclist = funclist

        global points
        X = points[:, 0]
        Y = points[:, 1]
        self.xmax = max(X)
        self.xmin = min(X)
        self.ymax = max(Y)
        self.ymin = min(Y)
        spanx = self.xmax - self.xmin
        spany = self.ymax - self.ymin
        #因为要画圆所以必须xy轴单位长度比例为1 而数据集中xy的范围不确定 故需要放缩画布
        self.fig,self.ax = plt.subplots(figsize=(10*spanx/(spanx+spany), 10*spany/(spanx+spany)))

        self.xdata = []
        self.ydata = []
        self.line, = self.ax.plot([], [], color = 'cyan',linestyle = '-')
        #self.point, = self.ax.plot([], [], 'ro') 绘制顺序有问题 被遮挡
        self.arrow = []
        self.circle = []
        for i in range(Fn.N):
            self.circle.append(*self.ax.plot([],[],color = 'grey',alpha = .2))
            self.arrow.append(self.ax.quiver([],[],[],[], units = 'xy',scale = 1,facecolor='white', width=10))

    def init(self):
        #plt.grid(True)
        #self.ax.grid(which='major',axis='both',color='white',linestyle='-',linewidth=1,alpha = 0.3)
        # 改变坐标轴及原点显示位置
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.spines['left'].set_position(('data', 0))

        self.ax.axis('off')
        self.ax.axis('equal')
        #self.ax.set_xticks([0])    #没有刻度无法显示网格线
        #self.ax.set_yticks([])
        scale = 1.5

        self.ax.set_xlim(self.xmin*scale, self.xmax*scale)
        self.ax.set_ylim(self.ymin*scale, self.ymax*scale)
        #self.ax.patch.set_facecolor("gray") 背景颜色
        #self.ax.patch.set_alpha(0.5)

        '''
        1 函数有多个返回值时自动打包为tuple 故手动打包为tuple无影响
        2 *拆包不可单独使用，只能在tuple里用
        3 matplotlib体系中此函数返回值必须为可以画的对象 不能是含有对象的列表(后续无相关处理)
        '''
        return (self.line,*self.arrow,*self.circle)

    def update(self,t):
        circle = np.linspace(-pi,pi,100)
        x,y = F(t).real,F(t).imag
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)
        #self.point.set_data(x, y)

        xn = 0
        yn = 0
        for num in range(Fn.N): #后一个箭头起始位置为前一个箭头指向的位置
            fn = self.funclist[num]
            self.arrow[num].set_offsets([xn, yn])

            self.circle[num].set_data(xn + fn.r * np.cos(circle), yn + fn.r * np.sin(circle))
            xn1 = (fn.c * fn.f(t)).real
            yn1 = (fn.c * fn.f(t)).imag
            self.arrow[num].set_UVC(xn1, yn1)


            xn += xn1
            yn += yn1
        return (*self.circle,*self.arrow,self.line)

if __name__ == '__main__':
    svgPath = 'data.svg'
    os.system('node svgToft.js' + ' ' + svgPath)    #利用js处理svg数据
    ftPath = 'ft.txt'
    readData(ftPath)  #此处文件名应与js保存的文件吻合
    funclist = [Fn(0)]
    for num in range(1,Fn.N // 2 + 1):  #N个箭头以顺逆交替且转速变快的顺序绘制
        funclist.append(Fn(num))
        if Fn.N%2 or num < Fn.N//2:
            funclist.append(Fn(-num))
    funclist = compute(funclist)

    os.system('del' + ' ' + ftPath) #在readData后删会出现问题

    plt.style.use('dark_background')
    model = Animate(funclist)
    ani = FuncAnimation(model.fig, model.update, frames=np.arange(0, 2*T, deltat), init_func=model.init, blit=True, interval=20, repeat=False)
    #ani.save('sample4.gif', writer='pillow')

    plt.show()