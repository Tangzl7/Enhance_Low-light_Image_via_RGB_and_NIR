from util import *
from Deblur.LLT import enhancement


@app.route('/deblur', methods=['GET'])
def get_deblur():
    print('deblur')
    if os.path.exists('static/deblur/rgb.png'):
        rgb = cv2.imread('static/deblur/rgb.png')
    else:
        return {'code': -1}
    if os.path.exists('static/deblur/nir.png'):
        nir = cv2.imread('static/deblur/nir.png')[:, :, 0]
    else:
        return {'code': -1}
    result = enhancement(rgb, nir)
    path = 'static/deblur/enhancement.png'
    cv2.imwrite(path, result)
    return {'enhancement': path}