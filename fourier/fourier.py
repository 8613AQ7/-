'''
位置随时间的变化由给定的函数f(t)决定
周期同样由f(t)决定 若傅里叶级数中的周期与之不符会出问题
'''
from ft import f,T
from math import e,pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

i = 1j

class Fn:
    N = 7
    def __init__(self,n):
        self.f = lambda t:e**(n*2*pi/T*i*t)    #此处n的传递很关键 类似闭包写法
        self.f0 = lambda t:e**(-n*2*pi/T*i*t)   #令自己不动的函数 求c
        self.c = 0          #常量系数
        self.r = 0          #改箭头轨迹的半径(圆心会变)

def F(t):   #傅里叶级数
    res = 0
    for fn in funclist:
        res += fn.c * fn.f(t)
    return res

def compute():
    global fun
    for fn in funclist:
        deltat = 0.01
        for t in np.arange(0,T,deltat):
            fn.c += f(t)*fn.f0(t)*deltat
        fn.c /= T   #此处为推广 周期不为1时不满足公式
        fn.r = abs(fn.c)


class Animate:
    def __init__(self):
        self.fig,self.ax = plt.subplots()
        self.xdata = []
        self.ydata = []
        self.line, = self.ax.plot([], [], color = 'b',linestyle = '-')
        self.point, = self.ax.plot([], [], 'co')
        self.text = self.ax.text(0.05,0.95,"",color = 'blue',size = '15',transform = self.ax.transAxes)
        self.arrow = []
        self.circle = []
        for i in range(Fn.N):
            self.circle.append(*self.ax.plot([],[],color = 'cyan',alpha = .8))
            self.arrow.append(self.ax.quiver([],[],[],[], units = 'xy',scale = 1,facecolor='mediumslateblue', width=0.04))

    def init(self):
        # 改变坐标轴及原点显示位置
        self.ax.spines['right'].set_color('none')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['bottom'].set_position(('data', 0))
        self.ax.spines['left'].set_position(('data', 0))

        self.ax.axis('equal')
        lim = 3.5
        self.ax.set_xlim(-lim, lim)
        self.ax.set_ylim(-lim, lim)

        #self.ax.patch.set_facecolor("gray") 背景颜色
        #self.ax.patch.set_alpha(0.5)

        '''
        1 函数有多个返回值时自动打包为tuple 故手动打包为tuple无影响
        2 *拆包不可单独使用，只能在tuple里用
        3 matplotlib体系中此函数返回值必须为可以画的对象 不能是含有对象的列表(后续无相关处理)
        '''
        return (self.line,self.point,self.text,*self.arrow,*self.circle)

    def update(self,t):
        circle = np.linspace(-pi,pi,100)
        x,y = F(t).real,F(t).imag
        self.xdata.append(x)
        self.ydata.append(y)
        self.line.set_data(self.xdata, self.ydata)
        self.point.set_data(x, y)
        self.text.set_text('t='+str(round(t*100)/100))


        self.arrow[Fn.N//2].set_offsets([0,0])
        xn = funclist[Fn.N//2].c.real
        yn = funclist[Fn.N//2].c.imag
        self.arrow[Fn.N//2].set_UVC(xn,yn)

        self.circle[Fn.N//2].set_data(np.cos(circle),np.sin(circle))

        for num in range(Fn.N):
            fn = funclist[num]
            if num != Fn.N//2 :
                self.arrow[num].set_offsets([xn,yn])
                self.circle[num].set_data(xn+fn.r*np.cos(circle), yn+fn.r*np.sin(circle))
                xn1 = (fn.c*fn.f(t)).real
                yn1 = (fn.c*fn.f(t)).imag
                self.arrow[num].set_UVC(xn1, yn1)
                xn += xn1
                yn += yn1


        return (*self.circle,self.line,self.text,*self.arrow,self.point)

if __name__ == '__main__':
    funclist = []
    for num in range(-(Fn.N // 2), Fn.N // 2 + 1):
        funclist.append(Fn(num))

    compute()

    model = Animate()
    ani = FuncAnimation(model.fig, model.update, frames=np.arange(0, 2*T, 0.01), init_func=model.init, blit=True, interval=10, repeat=False)
    #ani.save('sample1.gif', writer='pillow')
    plt.show()