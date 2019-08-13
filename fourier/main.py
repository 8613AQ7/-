import sys
import matplotlib.pyplot as plt
from fourier import run

if __name__ == '__main__':
   try:
       N = int(sys.argv[1]) #用户根据图像复杂程度输入箭头数量
       command = sys.argv[2]
       if command != 'play' and command != 'save':  #逻辑上很多余 但执行ani所需时间太久 故先判断输入合法性
           raise Exception

       ani = run(N)
       if command == 'play':
           plt.show()
       elif command == 'save':
           ani.save('animation.gif', writer='pillow')

   except:
       print('N play/save')