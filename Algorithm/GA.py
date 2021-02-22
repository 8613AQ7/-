from random import randint,random
from math import log,pow,sin,cos
def f(x):   # 找函数fx的最大值
    fx = x+10*sin(5*x)+7*cos(4*x)+5
    return fx
left = 4   #考虑区间[left,right]
right = 9
precise = 3 # 保留小数点后3位

class Population:
    def __init__(self,size, pc, pm):
        self.size = size
        self.population = []
        self.chro_length = int(log((right-left)*pow(10,precise),2))+1   # 数据要求->状态数量->二进制位个数
        self.pc = pc    # crossover 交叉互换概率
        self.pm = pm    # mutation 变异概率

    def init(self):
        for i in range(self.size):
            a = randint(0,pow(2,self.chro_length)) # 找到0-2^n 与 left-right的映射
            a = str(bin(a))[2:] # 二进制
            chro = []
            for i in range(self.chro_length-len(a)):
                chro.append(0)
            for i in range(len(a)):
                chro.append(int(a[i]))
            self.population.append(chro)

    def chro2x(self,chro):
        strbi = ''.join([str(i) for i in chro])
        num = int(strbi,2)
        return left + (right - left)*num/pow(2,self.chro_length)

    def fitness(self,chro):
        x = self.chro2x(chro)
        return f(x)

    def select(self):
        chro_fitness = [self.fitness(chroi) for chroi in self.population]
        s = sum(chro_fitness)
        pi = [fi/s for fi in chro_fitness]
        pii = [pi[0]]    # 累计概率
        for i in range(1,len(pi)):
            pii.append(pi[i] + pii[i-1])

        count = 0
        father = []
        while(count < self.size):
            r = random()
            if r<=pii[0]:
                father.append(self.population[0])
            else:
                index = 0
                while index < len(pii):
                    if pii[index]< r <= pii[index+1]:
                        break
                    index += 1

                father.append(self.population[index+1])
            count += 1
        self.population = father

    def crossover(self):
        new_population = []     # 如果不使用新列表存 而是直接在原来的population列表进行修改 则会导致刚交换的基因序列被再次交换 在不符合生物事实的同时会引起奇怪的问题
        for i in range(self.size-1):
            if random() < self.pc:
                point = randint(1,self.chro_length-1)
                new_population.append(self.population[i][:point]+self.population[i+1][point:])
            else:
                new_population.append(self.population[i])
        self.population = new_population

    def mutation(self):
        for chro in self.population:
            if random()<self.pm:
                point = randint(0, self.chro_length - 1)
                chro[point] = 1 - chro[point]

    def evolve(self,time):
        for i in range(time):
            self.select()
            self.crossover()
            self.mutation()

pop = Population(100,0.7,0.01)
pop.init()
pop.evolve(100)
print([pop.chro2x(i) for i in pop.population])