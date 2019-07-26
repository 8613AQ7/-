import imageio

def makegif():
    frames = []
    for i in range(8):
        pic = imageio.imread(str(i)+'.0.png')
        frames.append(pic)

    imageio.mimsave('wave.gif', frames, 'GIF', duration = 0.1)

if __name__ == '__main__':
    makegif()
