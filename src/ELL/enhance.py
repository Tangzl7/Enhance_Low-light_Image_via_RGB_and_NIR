import cv2
import numpy as np
import matlab.engine
from src.ELL.dehz import *
from src.Deblur.LLT import enhancement as deblur


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


def light_enhance(img, nir):
    img, nir = np.float32(img), np.float32(nir)
    clear_img = deblur(img, nir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imwrite('light.png', np.uint8(hsv[:, :, 2]))

    reflection_model_ = reflection_model_init(hsv[:, :, 2], nir)
    reflection_model_ = np.clip(reflection_model_, 0, 1)
    reflection_model_ = cv2.GaussianBlur(reflection_model_, (5, 5), 0)
    cv2.imwrite('tt.png', np.uint8(reflection_model_*255))

    hsv[:, :, 2] = hsv[:, :, 2] * (1 - reflection_model_) + nir * (reflection_model_)

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    # clear_img = np.float32(cv2.imread('../Deblur/t.png'))
    reflection_model_ = np.expand_dims(reflection_model_, axis=-1)
    img = np.where(reflection_model_ == 0, clear_img, img)
    return img


def enhancement(img, nir):
    img, nir = np.float32(img), np.float32(nir)
    clear_img = deblur(img, nir)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    reflection_model_ = reflection_model_init(hsv[:, :, 2], nir)
    reflection_model_ = np.clip(reflection_model_, 0, 1)
    cv2.imwrite('../Interface/static/low_light_enhancement/reflection_model.png', np.uint8(reflection_model_*255))
    reflection_model_ = cv2.GaussianBlur(reflection_model_, (5, 5), 0)

    hsv[:, :, 2] = hsv[:, :, 2] * (1 - reflection_model_) + nir * (reflection_model_)
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    reflection_model_ = np.expand_dims(reflection_model_, axis=-1)
    result = np.where(reflection_model_ == 0, clear_img, result)

    result = np.minimum(255, np.maximum(0, result))
    result = np.uint8(result)
    cv2.imwrite('../Interface/static/low_light_enhancement/result1.png', result)
    return result


def gradient_map(img):
    img = np.float32(img)
    gradient_x = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gradient_y = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    gradient_map = ((gradient_x ** 2) + (gradient_y ** 2)) ** 0.5

    return gradient_map


def enhance(rgb_path, nir_path):
    rgb = cv2.imread(rgb_path)
    nir = cv2.imread(nir_path)[:, :, 0]
    enhancement(rgb, nir)

    eng = matlab.engine.start_matlab()
    eng.ELL('../Interface/static/low_light_enhancement/result1.png', nir_path, '../Interface/static/low_light_enhancement/result2.png')

    result = deHaze(cv2.imread('../Interface/static/low_light_enhancement/result2.png') / 255.0, nir_path=nir_path) * 255
    cv2.imwrite('../Interface/static/low_light_enhancement/enhancement.png', result)

