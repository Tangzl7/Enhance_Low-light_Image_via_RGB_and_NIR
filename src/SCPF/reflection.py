import cv2
import numpy as np

def reflection_model_init(img, nir):
    img, nir = np.float32(img), np.float32(nir)
    b, g, r = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    wr = img.copy()
    wr[:, :, 2] = (nir - r) / (nir + r)
    wr[:, :, 1] = (nir - g) / (nir + g)
    wr[:, :, 0] = (nir - b) / (nir + b)
    return wr


def reflection_model(wr):
    for i in range(3):
        wr[:, :, i] = (wr[:, :, i] - wr[:, :, i].min()) / (wr[:, :, i].max() - wr[:, :, i].min())
    cv2.imwrite('../Interface/static/detail_enhancement/r_reflection_weight.png', np.uint8(wr[:, :, 2] * 255))
    return wr


def light_enhance(img, nir):
    img, nir = np.float32(img), np.float32(nir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    light = hsv[:, :, 2]
    sub_map = nir - light
    reflection = ((nir - light) - sub_map.min()) / (sub_map.max() - sub_map.min())
    hsv[:, :, 2] = reflection * light + nir * (1 - reflection)
    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img