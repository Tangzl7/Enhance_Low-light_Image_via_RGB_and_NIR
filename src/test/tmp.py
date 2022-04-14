import cv2
import numpy as np


def hpf(img, kernel_size=25):
    gaussian = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    img, gaussian = np.float32(img), np.float32(gaussian)
    hpf = np.abs(img - gaussian)
    cv2.imshow('r', np.uint8(gaussian))
    return hpf


def reflection_model_init(img, nir):
    img, nir = np.float32(img), np.float32(nir)
    # b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    # wr = img.copy()
    # wr[:, :, 2] = (nir - r) / (nir + r)
    # wr[:, :, 1] = (nir - g) / (nir + g)
    # wr[:, :, 0] = (nir - b) / (nir + b)
    return (nir - img) / (nir + img)


def reflection_model(wr):
    # for i in range(1):
    wr[:, :] = (wr[:, :] - wr[:, :].min()) / (wr[:, :].max() - wr[:, :].min())
    return wr


def light_enhance(img, nir, re):
    img, nir = np.float32(img), np.float32(nir)
    # img, nir = img[0:250, :], nir[:250, :]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    reflection_model_ = reflection_model_init(hsv[:, :, 2], nir)
    # reflection_model_ = reflection_model(reflection_model_)
    cv2.imshow('t', np.uint8(reflection_model_*255))
    cv2.waitKey(0)
    cv2.imwrite('tt.png', np.uint8(reflection_model_*255))

    light = hsv[:, :, 2]
    sub_map = np.abs(nir - light)
    sub_map = cv2.GaussianBlur(sub_map, (5, 5), 0)
    # sub_map = np.clip(sub_map, 0, 256)
    # reflection = ((nir - light) - sub_map.min()) / (sub_map.max() - sub_map.min())
    # reflection = np.clip(reflection, 0, 1)
    # hsv[:, :, 2] = (1 - reflection) * light + nir * (reflection)
    # sub_map[re <= 0] = 0
    hsv[:, :, 2] += sub_map
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img

def enhancement(vis, nir, re):
    # vis = cv2.imread('../../data/visual_results/full_resolution_images_of_fig_3_and_4/fig_4_a_rgb.tiff')
    # nir = cv2.imread('../../data/visual_results/full_resolution_images_of_fig_3_and_4/fig_4_a_nir.tiff')[:, :, 0]

    # reflection model
    vis = light_enhance(vis, nir, re)
    result = np.minimum(255, np.maximum(0, vis))
    result = np.uint8(result)
    cv2.imwrite('result1.png', result)


def gradient_map(img):
    img = np.float32(img)
    gradient_x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gradient_y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    gradient_map = ((gradient_x ** 2) + (gradient_y ** 2)) ** 0.5

    # cv2.imshow('t', np.uint8(gradient_map))
    # cv2.waitKey(0)
    return gradient_map


rgb = cv2.imread('639_rgb.bmp')
hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
nir = cv2.imread('639_nir.bmp')[:, :, 0]

g1 = gradient_map(hsv[:, :, 2])
# cv2.imshow('g', hsv[:, :, 2])
# cv2.waitKey(0)
g2 = gradient_map(nir)
re = np.float32(g2) - np.float32(g1)
re = np.clip(re, 0, 256)
# cv2.imshow('g', np.uint8(re))
# cv2.waitKey(0)
enhancement(rgb, nir, re)