import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.pyplot import quiver

'''
class quiver198(quiver):
    def __init__(self, ax, *args,scale=None, headwidth=3, headlength=5, headaxislength=4.5,minshaft=1, minlength=1, units='width', scale_units=None,angles='uv', width=None, color='k', pivot='tail', **kw):
        super(quiver198, self).__init__(ax, *args,scale, headwidth, headlength, headaxislength,inshaft, minlength, units, scale_units,angles, width, color, pivot, **kw)
'''
#a大小始终为1 方向与速度方向垂直
dt = 0.001
interval = 100
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




fig, ax = plt.subplots()
xdata, ydata = [], []
line, = ax.plot([], [], 'b-', animated=False)
point, = ax.plot([],[],'ro')
arrowv = ax.quiver([],[],[],[],scale = 40,facecolor='deeppink', linewidth=.5)
arrowa = ax.quiver([],[],[],[], scale = 10,facecolor='green', linewidth=.5)
def init():
    # 改变坐标轴及原点显示位置
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data', 0))
    ax.spines['left'].set_position(('data', 0))

    # ax.text(0, 0, u'a大小不变 始终与v垂直')
    ax.axis('equal')
    ax.set_xlim(min(sx) * 1.5, max(sx) * 1.5)
    ax.set_ylim(min(sy) * 1.5, max(sy) * 1.5)
    return line,

def update(frame):
    index = frame * interval
    xdata.append(sx[index])
    ydata.append(sy[index])
    line.set_data(xdata, ydata)

    arrowv.set_offsets([sx[index],sy[index]])
    arrowv.set_UVC(vxl[index],vyl[index])

    arrowa.set_offsets([sx[index], sy[index]])
    arrowa.set_UVC(axl[index], ayl[index])

    point.set_data(sx[index],sy[index])
    return line, arrowv, arrowa,point

'''
dt太小 出现误差 轨迹稍偏离圆
dt太大 动画太慢

选择小dt 间隔选取坐标制作动画


'''

if __name__ == '__main__':
    move()

    ani = FuncAnimation(fig, update,frames=range(len(sx)//interval),init_func=init, blit=True,interval = 10,repeat=False)
    ani.save('save.gif',writer = 'pillow')
    #plt.show()

