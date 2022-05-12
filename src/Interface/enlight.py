import os
import cv2
import matlab
import numpy as np
import matlab.engine

from util import *
from src.ELL.enhance import enhance

eng = matlab.engine.start_matlab()

@app.route('/enlight', methods=['GET'])
def get_enlight():
    print('enlight')
    rgb_path = 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/rgb.png'
    nir_path = 'D:/PycharmProjects/Enhance_Low-light_Image_via_RGB_and_NIR/src/Interface/static/low_light_enhancement/nir.png'
    if not os.path.exists('static/low_light_enhancement/rgb.png'):
        return {'code': -1}
    if not os.path.exists('static/low_light_enhancement/nir.png'):
        return {'code': -1}
    enhance(rgb_path, nir_path)
    return {'enhancement': 'static/low_light_enhancement/enhancement.png'}
