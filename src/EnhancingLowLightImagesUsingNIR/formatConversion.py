import numpy as np
import cv2


def rgb2yiq(img):
    img = np.double(img)
    b, g, r = cv2.split(img)
    y = 0.299 * r + 0.587 * g + 0.114 * b
    i = 0.595716 * r - 0.274453 * g - 0.321263 * b
    q = 0.211456 * r - 0.522591 * g + 0.311135 * b
    img[:, :, 0] = y
    img[:, :, 1] = i
    img[:, :, 2] = q
    return img


def yiq2rgb(img):
    img = np.double(img)
    y, i, q = cv2.split(img)
    r = 1 * y + 0.9563 * i + 0.6210 * q
    g = 1 * y - 0.2721 * i - 0.6474 * q
    b = 1 * y - 1.1070 * i + 1.7046 * q
    img[:, :, 0] = b
    img[:, :, 1] = g
    img[:, :, 2] = r
    return img