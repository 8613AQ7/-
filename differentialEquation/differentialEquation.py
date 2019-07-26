import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

'''
简谐振动 F = -kx 位移 速度 加速度之间存在复杂关系
位移 位移对时间一阶导 位移对时间二阶导 满足等式 即微分方程
用相图表示

理论上 不考虑摩擦力损失能量时 简谐运动会持续进行下去 即轨迹为椭圆 不向原点(平衡位置)靠拢
而计算时以极小时间内的平均速度代替了前一点的瞬时速度 导致误差
'''
T = 30 #过程持续时间
t = 0.01#单位时间

x0 = 0
v0 = 20
k = 1 #弹性系数
m = 1 #物体质量
u = 0.1#摩擦因数
g = 10 #重力加速度

xl = []
yl = []

def geta(x,v):  
    f1 = u * m * g #摩擦力
    if v > 0 :
        f1 = - f1
    if abs(v)<0.01:
        f1 = 0
    f2 = -k * x     #回复力
    
    f = f1 + f2

    return f/m #计算出加速度
    

def process():
    x = x0
    v = v0
    count = 0
    while abs(abs(x)-u*m*g/k) > 0.5 or abs(v)>0.1:   #收敛
        
        a = geta(x,v)   #根据公式计算加速度
        x += v * t      #根据定义式计算位移 速度
        v += a * t

        xl.append(x)
        yl.append(v)
   
def nextLocation(x,v):
    a = geta(x,v)
    return x + v * 0.0001,v + a * 0.0001
    
def arrow(xm,vm):
    #由于某些系数确定 当x与v确定时运动确定 在平面上均匀取点绘制矢量
    X = []
    Y = []
    U = []
    V = []
    for x in np.arange(-xm,xm+1,xm/5):
        for v in np.arange(-vm,vm+1,vm/5):
            x1,v1 = nextLocation(x,v)
            X.append(x)
            Y.append(v)
            U.append(x1-x)
            V.append(v1-v)
    X = np.array([X])
    Y = np.array([Y])
    


    c = []
    for i in range(len(U)):     #长度均缩放为1 颜色表示大小
        s = np.sqrt(U[i]**2+V[i]**2)
        c.append(s)
        U[i] /= s
        V[i] /= s

    
    #plt.quiver(X,Y,U,V,c, alpha=.5)#颜色
    plt.quiver(X,Y,U,V, edgecolor='k', facecolor='None', linewidth=.5)#边框

    #改变坐标轴及原点显示位置
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data',0))
    ax.spines['left'].set_position(('data',0))


fig, axx = plt.subplots()
xdata, ydata = [], []
ln, = axx.plot([], [], 'b-', animated=False)

def init():

    return ln,
    

def update(frame):
    xdata.append(xl[frame])
    ydata.append(yl[frame])
    ln.set_data(xdata, ydata)
    return ln,



if __name__ == '__main__':
    process()
    #plt.plot(xl,yl)

    vani = FuncAnimation(fig, update, frames=range(len(xl)),
                    init_func=init, blit=True,interval = 1,repeat=False)
    
    arrow(max(xl),max(yl))
    plt.show()
