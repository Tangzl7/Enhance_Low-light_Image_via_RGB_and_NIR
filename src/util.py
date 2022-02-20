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


# show_rgb_one('../data/demo/img_2_0.png', 2)
# show_rgb_light('../data/demo/img_2_0.png')
# show_rgb('../data/demo/img_2_0.png')
# show_nir('../data/demo/img_2_1.png')

# show_light_img('../data/demo/img_2_0.png')
# histogram('../src/LIME/enhanced_img_2_0.png')
result = hisEqulColor('../src/LIME/enhanced_img_2_0.png')
cv2.imwrite('result__.png', result)

# img = cv2.imread("../src/LIME/enhanced_img_2_0.png")
# b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
# b_prob = pixel_probability(b)
# g_prob = pixel_probability(g)
# r_prob = pixel_probability(r)
# b = probability_to_histogram(b, b_prob)
# g = probability_to_histogram(g, g_prob)
# r = probability_to_histogram(r, r_prob)
# cv2.imwrite('result_.png', img)