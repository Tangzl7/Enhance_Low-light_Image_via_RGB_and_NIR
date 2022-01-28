import cv2
import numpy as np


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


# show_rgb_one('../data/demo/img_2_0.png', 2)
# show_rgb_light('../data/demo/img_2_0.png')
# show_rgb('../data/demo/img_2_0.png')
# show_nir('../data/demo/img_2_1.png')

show_light_img('../data/demo/img_2_0.png')