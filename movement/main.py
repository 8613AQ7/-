import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
#a大小始终为1 方向与速度方向垂直
dt = 0.001
sx = []
sy = []
axl = []
ayl = []
vxl = []
vyl = []

def geta(v):
    vx,vy = v
    if vx == 0:
        ay = 0
        ax = 1 if vy < 0 else -1
    if vy == 0:
        ax = 0
        ay = 1 if vx > 0 else -1
    else:
        vx2 = vx**2
        vy2 = vy**2
        ax = (vy2/(vx2+vy2))**0.5
        ay = (vx2/(vy2+vx2))**0.5

    ax = ax if vy < 0 else -ax
    ay = ay if vx > 0 else -ay

    axl.append(ax)
    ayl.append(ay)
    a = [ax,ay]
    return a

def getv(v):
    a = geta(v)
    v = [v[i] + a[i] * dt for i in range(2)]
    vxl.append(v[0])
    vyl.append(v[1])
    return v

def gets(s,v):
    s = [s[i] + v[i] * dt for i in range(2)]
    return s


def move():

    s0 = [0,-25] #a = v2/r
    v0 = [5,0]

    s = s0
    v = v0
    for t in np.arange(0,40,dt):
        sx.append(s[0])
        sy.append(s[1])
        s = gets(s,v)
        v = getv(v)




fig, axx = plt.subplots()
xdata, ydata = [], []
ln, = axx.plot([], [], 'b-', animated=False)

def init():

    return ln,
    
interval = 100
def update(frame):
    index = frame * interval
    xdata.append(sx[index])
    ydata.append(sy[index])
    ln.set_data(xdata, ydata)

    arrowv = plt.quiver(sx[index],sy[index],vxl[index],vyl[index], scale = 40,facecolor='deeppink', linewidth=.5)
    arrowa = plt.quiver(sx[index],sy[index],axl[index],ayl[index], scale = 10,facecolor='green', linewidth=.5)

    point = plt.scatter(sx[index],sy[index],color = 'red')
    return ln,arrowv,arrowa,point

def update2(frame):
    xdata.append(axl[frame*10])
    ydata.append(ayl[frame*10])
    ln.set_data(xdata, ydata)
    return ln,


'''
dt太小 出现误差 轨迹稍偏离圆
dt太大 动画太慢

选择小dt 间隔选取坐标制作动画


'''

if __name__ == '__main__':
    move()
    #plt.plot(xl,yl)
    #改变坐标轴及原点显示位置
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data',0))
    ax.spines['left'].set_position(('data',0))

    #ax.text(0, 0, u'a大小不变 始终与v垂直')
    plt.axis('equal')
    plt.xlim(min(sx) * 1.5,max(sx) * 1.5)
    plt.ylim(min(sy) * 1.5,max(sy) * 1.5)
    a = list(range(len(sx)//interval))
    ani = FuncAnimation(fig, update,init_func=init, blit=True,interval = 10,repeat=False)
    #ani.save('gif.gif',writer='pillow')
    plt.show()
