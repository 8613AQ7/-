import imageio

def makegif(n):
    frames = []
    for i in range(n):
        pic = imageio.imread(str(i)+'.png')
        frames.append(pic)

    imageio.mimsave('move.gif', frames, 'GIF', duration = 0.01)

if __name__ == '__main__':
    makegif(50)
