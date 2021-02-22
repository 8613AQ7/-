from math import sin,cos,exp
from random import random

'''
重要参数：T初始值(太活跃) 终止值 降低速率a(越慢越好)
随机扰动的方式delx (此例中delx越大 结果提升明显)

'''
def f(x):   # 找函数fx的最小值
    return x+3*sin(x)-7*cos(2*x)
left = 8    # 考虑区间[left,right]
right = 20

def substitute(de,T):   # dely<0说明更优 替换；dely>0 虽然不是更优 但可能在更远的地方存在更优解 故以一定概率替换
    if de<0:
        return True
    elif exp(-de/T) > random() :
        return True
    else:
        return False

def sa():
    T = 1e4    # 初始温度
    a = 0.999   # 温度降低的速度
    T_stop = 1e-5  # 终止的温度
    oldx = random()*(right-left)+left  # 随机选择初始值
    newx = oldx

    while T > T_stop:
        delx = (random()-0.5)*5     # 每次产生随机扰动 根据条件选择替换
        newx = oldx + delx
        if newx > right or newx < left:
            newx -= 2*delx

        dely = f(newx) - f(oldx)
        if(substitute(dely,T)):
            oldx = newx

        T *= a

    return oldx

correct = 0
testTime = 10
testAmount = 100
for i in range(testTime): # 多次测试正确概率取平均值
    correcti = 0
    for j in range(testAmount):    # 测试一次正确概率
        x = sa()
        if round(x*10)/10 == 9.5:
            correcti += 1
    correct += correcti/testAmount
correct /= testTime
print(correct)
