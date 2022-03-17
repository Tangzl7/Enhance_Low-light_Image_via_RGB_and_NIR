import os
import cv2
import matlab
import numpy as np
import matlab.engine

from util import *

eng = matlab.engine.start_matlab()

@app.route('/denoise', methods=['GET'])
def get_denoise():
    print('denoise')
    rgb_path = 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/denoise/rgb.png'
    nir_path = 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/denoise/nir.png'
    write_path = 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/denoise/enhancement.png'
    if not os.path.exists('static/denoise/rgb.png'):
        return {'code': -1}
    if not os.path.exists('static/denoise/nir.png'):
        return {'code': -1}
    eng.denoise(rgb_path, nir_path, write_path)
    return {'enhancement': 'static/dnoise/enhancement.png'}