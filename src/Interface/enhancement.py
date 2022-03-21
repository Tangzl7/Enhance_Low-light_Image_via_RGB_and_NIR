import os
import cv2
import random
from util import *
from SCPF.fusion import enhancement as enhancement


@app.route('/enhancement', methods=['GET'])
def get_enhancement():
    print('enhancement')
    if os.path.exists('static/detail_enhancement/rgb.png'):
        rgb = cv2.imread('static/detail_enhancement/rgb.png')
    else:
        return {'code': -1}
    if os.path.exists('static/detail_enhancement/nir.png'):
        nir = cv2.imread('static/detail_enhancement/nir.png')[:, :, 0]
    else:
        return {'code': -1}
    result = enhancement(rgb, nir)
    path = 'static/detail_enhancement/enhancement.png'
    cv2.imwrite(path, result)
    return {'enhancement': path}
