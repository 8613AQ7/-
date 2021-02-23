from PIL import Image
import numpy as np
'''
去噪声/压缩
'''
path = 'test.jpg'
origin_im = Image.open(path)

def SVD_Compress(image,k):
    '''
    image:图片格式
    k:选择多少个奇异值 k<min(m,n)
    '''
    origin_A = np.array(image)
    
    if k > origin_A.shape[0] or k > origin_A.shape[1]:
        raise KeyError
    
    processed_A = np.zeros_like(origin_A)
    for i in range(3):#RGB
        A = origin_A[:,:,i]
        
        U,S,VT = np.linalg.svd(A)
        S=np.diag(S)
        S.resize(A.shape)#在不考虑精度的情况下A=USVT
        
        U = U[:,:k]
        S = S[:k,:k]
        VT = VT[:k,:]#奇异值已经排过序了 越大越重要

        A1=np.dot(U,S)
        A1=np.dot(A1,VT)

        processed_A[:,:,i] = A1

    return Image.fromarray(processed_A)

#这样写效率很低 先得到完整的USVT再遍历k会好一点 但是为了保证函数的完整性
for k in [20,50,100,200,500,1000]:
    im = SVD_Compress(origin_im,k)
    im.save(path[:-4]+str(k)+path[-4:])
    print(k)

