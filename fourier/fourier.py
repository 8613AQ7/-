from math import e,pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

i = 1j
deltat = 0.01   #与js中相符
points = [] #定义ft
length = 0
xmax = xmin = ymax = ymin = 0 #绘图

class JS:   #运行js程序获取数据
    jsPath = 'svgToft.js'
    def __init__(self,N,T,svgPath):
        self.svgPath = svgPath
        self.txtPath = svgPath[:-4] + 'N=' + str(N) + 'T=' + str(T) + '.txt'
        self.T = T

    def _readData(self):
        global points,length,xmax,xmin,ymax,ymin
        with open(self.txtPath, 'r') as data:
            info = data.readline().split()
            while info:
                x, y = info
                points.append([float(x), float(y)])
                info = data.readline().split()

        length = len(points)
        points = np.array(points)
        X, Y = points[:, 0], points[:, 1]
        points = points - [np.median(X), np.median(Y)]  # 重心移动至原点附近 画图好看
        X, Y = points[:, 0], points[:, 1]  # 重新获取数据求最值
        xmax = max(X)
        xmin = min(X)
        ymax = max(Y)
        ymin = min(Y)

    def run(self):
        if not os.path.exists(self.txtPath):    #之前没有计算过此参数下的数据
            if os.path.exists(self.svgPath):    #用户输入路径正确
                os.system('node ' + JS.jsPath + ' ' + str(self.T) + ' ' + self.svgPath + ' ' + self.txtPath)    #此处js报错python无法拦截
            else:
                print('请输入正确svg文件路径')
                exit()
        self._readData()
        print('data ready')

class fn:#傅里叶级数中的每一项
    def __init__(self,n,T):
        self.f = lambda t:e**(n*2*pi/T*i*t)    #此处n的传递很关键 类似闭包写法
        self.f0 = lambda t:e**(-n*2*pi/T*i*t)   #令自己不动的函数 求c
        self.c = 0          #常量系数
        self.r = 0          #改箭头轨迹的半径(圆心会变)

class Fourier:   #一个傅里叶级数
    def __init__(self, N, T):
        self.N = N
        self.T = T
        self.fn = [fn(0,T)]
        for num in range(1, N // 2 + 1):  # N个箭头以顺逆交替且转速变快的顺序绘制
            self.fn.append(fn(num,T))
            if N % 2 or num < N // 2:
                self.fn.append(fn(-num,T))

    def f(self, t):  # 点的位置随时间变化（图像svg->txt给出）
        index = int(round(length * (t % self.T) / self.T))  # 映射关系
        return points[index][0] + points[index][1] * i

    def F(self, t):  # 点的位置随时间变化(由计算出的傅里叶级数拟合出)
        res = 0
        for fi in self.fn:
            res += fi.c * fi.f(t)
        return res

    def compute(self):  #计算系数c 从而得到Ft
        for fi in self.fn:
            for t in np.arange(0,self.T,deltat):
                fi.c += self.f(t)*fi.f0(t)*deltat
            fi.c /= self.T   #此处为推广 周期不为1时不满足公式
            fi.r = abs(fi.c)

class Animate:  #动画效果
    def __init__(self,F):
        self.F = F #傅里叶级数函数

        spanx = xmax - xmin
        spany = ymax - ymin
        #因为要画圆所以必须xy轴单位长度比例为1 而数据集中xy的范围不确定 故需要放缩画布
        self.fig,self.ax = plt.subplots(figsize=(10*spanx/(spanx+spany), 10*spany/(spanx+spany)))

        self.xdata = []
        self.ydata = []
        self.line, = self.ax.plot([], [], color = 'cyan',linestyle = '-')
        #self.point, = self.ax.plot([], [], 'ro') 绘制顺序有问题 被遮挡
        self.arrow = []
        self.circle = []
        for i in range(self.F.N):
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
        scale = 1.8

        self.ax.set_xlim(xmin*scale, xmax*scale)
        self.ax.set_ylim(ymin*scale, ymax*scale)

        '''
        1 函数有多个返回值时自动打包为tuple 故手动打包为tuple无影响
        2 *拆包不可单独使用，只能在tuple里用
        3 matplotlib体系中此函数返回值必须为可以画的对象 不能是含有对象的列表(后续无相关处理)
        '''
        return (self.line,*self.arrow,*self.circle)

    def update(self,t):
        circle = np.linspace(-pi,pi,100)
        x,y = self.F.F(t).real,self.F.F(t).imag
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)
        #self.point.set_data(x, y)

        xn = 0
        yn = 0
        for num in range(self.F.N): #后一个箭头起始位置为前一个箭头指向的位置
            fi = self.F.fn[num]
            self.arrow[num].set_offsets([xn, yn])

            self.circle[num].set_data(xn + fi.r * np.cos(circle), yn + fi.r * np.sin(circle))
            xn1 = (fi.c * fi.f(t)).real
            yn1 = (fi.c * fi.f(t)).imag
            self.arrow[num].set_UVC(xn1, yn1)
            xn += xn1
            yn += yn1
        return (*self.circle,*self.arrow,self.line)

def run(N,T,inputPath):
    js = JS(N,T,inputPath)
    js.run()
    fourier = Fourier(N,T)
    fourier.compute()
    print('compute finish')
    plt.style.use('dark_background')
    model = Animate(fourier)
    ani = FuncAnimation(model.fig, model.update, frames=np.arange(0, 2 * T, deltat), init_func=model.init, blit=True,interval=20, repeat=False)

    #ani.save(outputPath,writer= 'pillow')
    return ani


if __name__ == '__main__':
    run(10,2,'d123.svg','test.gif')
    plt.show()

