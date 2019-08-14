import sys
import matplotlib.pyplot as plt
from fourier import run

if __name__ == '__main__':
    try:
        N = int(sys.argv[1]) #用户根据图像复杂程度输入箭头数量
        T = int(sys.argv[2]) #周期（绘制速度）
        inputPath = sys.argv[3]
        outputPath = sys.argv[4]
    except:
        print('N T inputPath outputPath')
    else:
        ani = run(N,T,inputPath)
        print('writing-----')
        ani.save(outputPath,writer = 'pillow')
        print('complete')