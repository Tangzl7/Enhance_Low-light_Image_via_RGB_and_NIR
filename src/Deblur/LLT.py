import cv2
import numpy as np
from matplotlib import cm as CM
from matplotlib import pyplot as plt


def burred_nir(nir, kernel_size=19):
    return cv2.blur(nir, (kernel_size, kernel_size), 0)


def gradient_map(map):
    dx = cv2.Sobel(map, cv2.CV_32F, 1, 0)
    dy = cv2.Sobel(map, cv2.CV_32F, 0, 1)
    gradient = ((dx ** 2) + (dy ** 2)) ** 0.5
    return gradient


def laplacian(map):
    return cv2.Laplacian(map, cv2.CV_32F)


def llt(rgb, nir):
    lamb, beta = 0.1, 0.1
    llt_map = [[] for i in range(3)]
    for i in range(3):
        channel = rgb[:, :, i]
        gradient_channel = gradient_map(channel)
        gradient_nir = gradient_map(nir)
        # gradient_channel = np.uint8(gradient_channel * 2550)
        # cv2.imshow('g', gradient_channel)
        # cv2.waitKey(0)
        A = np.ones((rgb.shape[0], rgb.shape[1]), dtype=np.float32)
        B = np.zeros((rgb.shape[0], rgb.shape[1]), dtype=np.float32)

        for j in range(100):
            second_gradient_A = laplacian(A)
            second_gradient_B = laplacian(B)
            g_a = 2 * nir * (A * nir + B - channel) + \
                    2 * lamb * gradient_nir * (A * gradient_nir - gradient_channel) + \
                    2 * beta * second_gradient_A
            g_b = 2 * (A * nir + B - channel) + 2 * beta * second_gradient_B
            second_gradient_ga = laplacian(g_a)
            second_gradient_gb = laplacian(g_b)
            # l_a = np.sum(g_a * g_a) / np.sum(g_a * g_a * \
            #         (nir * nir + lamb * gradient_nir * gradient_nir + beta * second_gradient_ga * second_gradient_ga))
            # l_b = np.sum(g_b * g_b) / np.sum(g_b * (g_b + beta * second_gradient_gb))
            l_a = 0.02
            l_b = 0.02
            A -= l_a * g_a
            B -= l_b * g_b
            # if l_a < 1e-7 and l_b < 1e-7:
            #     break
        llt_map[i].append(A)
        llt_map[i].append(B)
    return llt_map


def enhancement(rgb, nir):
    burred = burred_nir(nir)
    cv2.imwrite('../Interface/static/deblur/blurred_nir.png', burred)
    rgb, nir, burred = np.float32(rgb), np.float32(nir), np.float32(burred)
    rgb, nir, burred = rgb / 255., nir / 255., burred / 255.
    llt_map = llt(rgb, burred)
    fig = plt.gcf()
    plt.imshow(llt_map[0][0], cmap=CM.hot)
    fig.savefig('../Interface/static/deblur/slope.png')
    fig = plt.gcf()
    plt.imshow(llt_map[0][1], cmap=CM.jet)
    fig.savefig('../Interface/static/deblur/offset.png')
    enhancement = rgb.copy()
    for i in range(3):
        enhancement[:, :, i] = llt_map[i][0] * nir + llt_map[i][1]
    enhancement *= 255
    enhancement = np.minimum(255, np.maximum(0, enhancement))
    enhancement = np.uint8(enhancement)
    return enhancement
