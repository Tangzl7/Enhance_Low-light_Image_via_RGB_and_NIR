import cv2
import numpy as np
from wlsFilter import wlsFilter
from dualWlsFilter import wlsFilter as dwlsFilter
from formatConversion import rgb2yiq, yiq2rgb


if __name__ == '__main__':
    I = np.double(cv2.resize(cv2.imread('../../data/demo/img_2_0.png'), (128, 128)))
    NIR = np.double(cv2.resize(cv2.imread('../../data/demo/img_2_1.png'), (128, 128)))[:, :, 0]


    NIR_wls = wlsFilter(NIR)
    NIR_detail = NIR/(NIR_wls + 0.0001)
    lambda_, alpha = 1, 2
    i1 = wlsFilter(I[:, :, 0], lambda_)
    i2 = wlsFilter(I[:, :, 1], lambda_)
    i3 = wlsFilter(I[:, :, 2], lambda_)
    denoise = np.concatenate((np.expand_dims(i1, axis=-1),
                              np.expand_dims(i2, axis=-1), np.expand_dims(i3, axis=-1)), axis=-1)
    denoise_yiq = rgb2yiq(denoise)
    denoise_y = denoise_yiq[:, :, 0]
    I_yiq = rgb2yiq(I)

    v_nir = dwlsFilter(I_yiq[:, :, 0], denoise_y, NIR, lambda_)
    yiq_result = np.concatenate((np.expand_dims(v_nir * NIR_detail, axis=-1), np.expand_dims(denoise_yiq[:, :, 1], axis=-1),
                                 np.expand_dims(denoise_yiq[:, :, 2], axis=-1)), axis=-1)
    rgb_result = yiq2rgb(yiq_result)
    cv2.imshow('result', rgb_result)
    cv2.waitKey(0)