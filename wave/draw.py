from matplotlib import pyplot as plt
import numpy as np
from getgif import makegif
points = []
#origins = [[0, 0]]
origins = [[-5, 0],[5,0]]
class Point():
    def __init__(self,x,y,b):
        self.x = x
        self.y = y
        self.a = 0
        for origin in origins:
            d = ((x - origin[0])**2 + (y - origin[1])**2)**0.5
            self.a += np.sin(2*d+b)

        self.c = str((self.a+2)/4)
        
def creat(b):
    span = 20
    delta = 0.2
    for i in np.arange(-span, span, delta):
        for j in np.arange(-span, span, delta):
            points.append(Point(i, j, b))

def draw():
    plt.scatter([p.x for p in points],[p.y for p in points],c=[p.c for p in points])
    '''
    for p in points:
        plt.scatter([p.x],[p.y],c = str((p.a+2)/4))
    '''
    plt.axis('off')
    #plt.show()


if __name__ == '__main__':
    '''
    creat(0)
    draw()
    '''
    for i in np.arange(0, np.pi * 2, np.pi/4):
        creat(7-i)
        draw()
        plt.savefig(str(i//(np.pi/4))+'.png')
        plt.clf()
        points.clear()
        print(i//(np.pi/4))
    
    makegif()
