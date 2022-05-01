import cv2
import numpy as np
import matplotlib.pylab as plt


def show_rgb(path):
    img = cv2.imread(path)
    b, g, r = img[:, :, 0].copy(), img[:, :, 1].copy(), img[:, :, 2].copy()
    r = np.dstack([np.zeros(r.shape, np.uint8), np.zeros(r.shape, np.uint8), r])
    g = np.dstack([np.zeros(g.shape, np.uint8), g, np.zeros(g.shape, np.uint8)])
    b = np.dstack([b, np.zeros(b.shape, np.uint8), np.zeros(b.shape, np.uint8)])
    img_rgb = np.hstack([r, g, b])
    cv2.namedWindow('rgb', 0)
    cv2.imshow('rgb', img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_nir(path):
    img = cv2.imread(path)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, 0] <= 200:
                img[i, j, :] = 0
    cv2.namedWindow('nir', 0)
    cv2.imshow('nir', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_rgb_one(path, channel):
    img_org = cv2.imread(path)
    img = img_org[:, :, channel:channel+1].copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, 0] <= 250 or img_org[i, j, 0] > 200 or img_org[i, j, 1] > 200:
                img[i, j, :] = 0
    cv2.namedWindow('rgb_one', 0)
    cv2.imshow('rgb_one', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_rgb_light(path):
    img = cv2.imread(path)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, 0] <= 200 or img[i, j, 1] <= 200 or img[i, j, 2] <= 200:
                img[i, j, :] = 0
    cv2.namedWindow('light', 0)
    cv2.imshow('light', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_light_img(path):
    img = cv2.imread(path)
    light = np.zeros([img.shape[0], img.shape[1], 3], np.uint8)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            light[i, j, :] = 255 - max(img[i][j][0], img[i][j][1], img[i][j][2])
    cv2.namedWindow('light', 0)
    cv2.imshow('light', light)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_channel_img(path, i):
    img = cv2.imread(path)
    return img[:, :, i]


def histogram(path):
    img = cv2.imread(path)
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    plt.figure('img')
    ar = np.array(r).flatten()
    plt.hist(ar, bins=256, facecolor='r', edgecolor='r')
    ag = np.array(g).flatten()
    plt.hist(ag, bins=256, facecolor='g', edgecolor='g')
    ab = np.array(b).flatten()
    plt.hist(ab, bins=256, facecolor='b', edgecolor='b')
    plt.show()


def pixel_probability(img):
    prob = np.zeros(shape=(256))

    for rv in img:
        for cv in rv:
            prob[cv] += 1

    r, c = img.shape
    prob = prob / (r * c)
    return prob


def probability_to_histogram(img, prob):
    prob = np.cumsum(prob)

    img_map = [int(i * prob[i]) for i in range(256)]

    r, c = img.shape
    for ri in range(r):
        for ci in range(c):
            img[ri, ci] = img_map[img[ri, ci]]
    return img

def hisEqulColor(path):
    img = cv2.imread(path)
    yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    channels = cv2.split(yuv)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, yuv)
    cv2.cvtColor(yuv, cv2.COLOR_YCR_CB2BGR, img)
    return img

def zmMinFilterGray(src, r=7):
    '''最小值滤波，r是滤波器半径'''
    '''if r <= 0:
      return src
    h, w = src.shape[:2]
    I = src
    res = np.minimum(I , I[[0]+range(h-1) , :])
    res = np.minimum(res, I[range(1,h)+[h-1], :])
    I = res
    res = np.minimum(I , I[:, [0]+range(w-1)])
    res = np.minimum(res, I[:, range(1,w)+[w-1]])
    return zmMinFilterGray(res, r-1)'''
    return cv2.erode(src, np.ones((2 * r + 1, 2 * r + 1)))  # 使用opencv的erode函数更高效


def guidedfilter(I, p, r, eps):
    '''引导滤波，直接参考网上的matlab代码'''
    height, width = I.shape
    m_I = cv2.boxFilter(I, -1, (r, r))
    m_p = cv2.boxFilter(p, -1, (r, r))
    m_Ip = cv2.boxFilter(I * p, -1, (r, r))
    cov_Ip = m_Ip - m_I * m_p

    m_II = cv2.boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I

    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I

    m_a = cv2.boxFilter(a, -1, (r, r))
    m_b = cv2.boxFilter(b, -1, (r, r))
    return m_a * I + m_b


def getV1(m, r, eps, w, maxV1):  # 输入rgb图像，值范围[0,1]
    '''计算大气遮罩图像V1和光照值A, V1 = 1-t/A'''
    V1 = np.min(m, 2)  # 得到暗通道图像
    V1 = guidedfilter(V1, zmMinFilterGray(V1, 7), r, eps)  # 使用引导滤波优化
    bins = 2000
    ht = np.histogram(V1, bins)  # 计算大气光照A
    d = np.cumsum(ht[0]) / float(V1.size)
    for lmax in range(bins - 1, 0, -1):
        if d[lmax] <= 0.999:
            break
    A = np.mean(m, 2)[V1 >= ht[1][lmax]].max()
    print(A)

    V1 = np.minimum(V1 * w, maxV1)  # 对值范围进行限制

    return V1, A

def getV1_(m, r, eps, w, maxV1):  # 输入rgb图像，值范围[0,1]
    '''计算大气遮罩图像V1和光照值A, V1 = 1-t/A'''
    img = cv2.imread('../Interface/static/low_light_enhancement/init_enhancement.png')
    nir = cv2.imread('../test/80_nir.bmp')[:, :, 0] / 256.0
    il = cv2.imread('../Interface/static/low_light_enhancement//init_illumination.png')[:, :, 0] / 256.0
    nir = np.uint8(nir / (il ** 0.7) * 256)
    diff = np.abs(nir * 1.0 - img[:, :, 0] * 1.0) / 255.
    # diff = np.uint8(diff)
    dens_map = img.min(axis=-1) / 255.
    dens_map = np.minimum(diff, dens_map)

    V1 = np.min(m, 2)  # 得到暗通道图像
    V1 = guidedfilter(V1, zmMinFilterGray(V1, 7), r, eps)  # 使用引导滤波优化
    dens_map = guidedfilter(dens_map, zmMinFilterGray(dens_map, 7), r, eps)  # 使用引导滤波优化
    bins = 2000
    ht = np.histogram(dens_map, bins)  # 计算大气光照A
    d = np.cumsum(ht[0]) / float(dens_map.size)
    for lmax in range(bins - 1, 0, -1):
        if d[lmax] <= 0.999:
            break
    A = np.mean(m, 2)[dens_map >= ht[1][lmax]].mean()

    V1 = np.minimum(V1 * w, maxV1)  # 对值范围进行限制
    print(A)

    return V1, A


def deHaze(m, r=81, eps=0.001, w=0.95, maxV1=0.80, bGamma=False):
    Y = np.zeros(m.shape)
    V1, A = getV1(m, r, eps, w, maxV1)  # 得到遮罩图像和大气光照
    for k in range(3):
        Y[:, :, k] = (m[:, :, k] - V1) / (1 - V1 / A)  # 颜色校正
    Y = np.clip(Y, 0, 1)
    if bGamma:
        Y = Y ** (np.log(0.5) / np.log(Y.mean()))  # gamma校正,默认不进行该操作
    return Y


if __name__ == '__main__':
    m = deHaze(cv2.imread('D:/MATLAB/bin/denoisy/init_enhancement.png') / 255.0) * 255
    cv2.imwrite('defog_.png', m)
    # rawImg = np.fromfile('./tmp.raw', dtype='uint16')
    # img = rawImg.reshape(1080, 1920, 1)
    # m = cv2.imread('D:/MATLAB/bin/tmp.raw')
    # m = cv2.cvtColor(img, cv2.COLOR_BayerGR2BGR)
    # m = np.uint8(m)
    # cv2.imwrite('t.png', img)
    # cv2.imshow('f', img)
    # cv2.waitKey(0)
    # pass
    # rawImg = np.fromfile('D:/MATLAB/bin/denoisy/tmp.raw', dtype='uint16')
    # rawImg = rawImg.reshape(1080, 1920, 1)
    # cv2.imwrite('t_nir.png', rawImg)
    # cv2.imshow('f', rawImg)
    # cv2.waitKey(0)

