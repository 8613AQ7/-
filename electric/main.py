import matplotlib.pyplot as plt
import numpy as np
k = 1e3 # 9* 10^9 太大 大小不影响比例
points=[]
class Q:
    def __init__(self,x ,y , q):
        self.x = x
        self.y = y
        self.q = q

qs = [Q(-1,0,1),Q(1,0,1)]
class Point:
    def __init__(self, x, y,f):
        self.x = x
        self.y = y
        self.e = [0,0]
        self.f = 0
        if f:
            for q in qs:
                dx = x - q.x
                dy = y - q.y
                r2 = dx**2 + dy**2  # 无穷大由python自行处理
                intense = k * q.q / r2
                self.e[0] += dx / r2**0.5 * intense
                self.e[1] += dy / r2**0.5 * intense

                self.f += k * q.q / r2**0.5

    def show(self):
        print(self.x, self.y, self.e, self.f)

def fToc(e):
    acti = 1/(1+np.e**(-e))
    return (acti+1)*0xFFFFFF//2

def create():
    span = 2
    delta = 0.2
    for i in np.arange(-span, span+delta, delta):
        i = round(i*100)/ 100.0
        for j in np.arange(-span, span+delta ,delta):
            j = round (j*100)/100.0
            points.append(Point(i,j,True))
            '''
            c = '#' + hex(int(fToc(points[-1].f)))[2:]
            plt.scatter(i, j, c = c )
            '''
def draw1(): # 电场线
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_position(('data',0))
    ax.spines['left'].set_position(('data',0))
    plt.xticks([])
    plt.yticks([])
    x = []
    y = []
    ex = []
    ey = []
    c = [] # 用颜色代替疏密表示大小
    for p in points:
        if p.e[0] :
            x.append(p.x)
            y.append(p.y)
            d = (p.e[0] **2 + p.e[1] ** 2)**0.5
            c.append(d)
            ex.append(p.e[0]/d)
            ey.append(p.e[1]/d)


    plt.quiver(x, y, ex, ey, c, alpha = 0.5)
    plt.quiver(x, y, ex, ey, edgecolor = 'k', facecolor = 'None', linewidth = 0.4)
    for q in qs:
        c = 'b' if q.q > 0 else 'r'
        plt.scatter([q.x],[q.y],c = c, linewidths=4)

def getindex(x,y):
    return int(round(105*(x + 2) + 5*(y + 2)))

lines = {'yellow':[],
         'green':[],
         'purple':[],
         'orange':[]}
def draw2(): # 等势线
    for p in points:
        if abs(p.f - points[getindex(0,0)].f) < 10:
            pass
            # plt.scatter(p.x,p.y,c = 'black')
        elif abs(p.f - points[getindex(1.48,0)].f) < 50:
            plt.scatter(p.x , p.y, c = 'yellow')
            lines['yellow'].append(p)
        elif abs(p.f - points[getindex(1.45,0)].f) < 80:
            plt.scatter(p.x, p.y, c='green')
            lines['green'].append(p)
        elif abs(p.f - points[getindex(0.6,0)].f) < 500:
            plt.scatter(p.x, p.y, c='purple')
            lines['purple'].append(p)
        elif abs(p.f - points[getindex(0.2,0)].f) < 150:
            plt.scatter(p.x, p.y, c='orange')
            lines['orange'].append(p)
def draw3(f,c): #连接等势点
    cmp = lambda p: np.arctan(p.y / p.x)
    fi = []
    fi.append(list(filter(lambda p:p.x> 0 and p.y > 0, f)))
    fi.append(list(filter(lambda p: p.x < 0 and p.y > 0, f)))
    fi.append(list(filter(lambda p: p.x > 0 and p.y < 0, f)))
    fi.append(list(filter(lambda p: p.x < 0 and p.y < 0, f)))
    for i in fi:
        i.sort(key = cmp)
        i[0].show()
        i[-1].show()
        plt.plot([p.x for p in i], [p.y for p in i], c=c)


create()
draw1()
draw2()
'''
for color in lines:
    draw3(lines[color],color)
'''
plt.show()

#points[a].show()

#plt.savefig('等量同种.png')
