import os
import cv2
import random
from flask import Flask, request
app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ


@app.route('/get_rgb_img', methods=['POST'])
def get_rgb_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/detail_enhancement/rgb.png')
    return {'code': 200, 'rgb': 'http://127.0.0.1:5590/static/detail_enhancement/rgb.png'}


@app.route('/get_nir_img', methods=['POST'])
def get_nir_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/detail_enhancement/nir.png')
    return {'code': 200, 'nir': 'http://127.0.0.1:5590/static/detail_enhancement/nir.png'}


@app.route('/blur_rgb_img', methods=['POST'])
def blur_rgb_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/deblur/rgb.png')
    return {'code': 200, 'rgb': 'http://127.0.0.1:5590/static/deblur/rgb.png'}


@app.route('/sharp_nir_img', methods=['POST'])
def sharp_nir_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/deblur/nir.png')
    return {'code': 200, 'nir': 'http://127.0.0.1:5590/static/deblur/nir.png'}


@app.route('/noisy_rgb_img', methods=['POST'])
def noisy_rgb_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/denoise/rgb.png')
    return {'code': 200, 'rgb': 'http://127.0.0.1:5590/static/denoise/rgb.png'}


@app.route('/clear_nir_img', methods=['POST'])
def clear_nir_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/denoise/nir.png')
    return {'code': 200, 'nir': 'http://127.0.0.1:5590/static/denoise/nir.png'}


@app.route('/low_light_rgb_img', methods=['POST'])
def low_light_rgb_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/low_light_enhancement/rgb.png')
    return {'code': 200, 'rgb': 'http://127.0.0.1:5590/static/low_light_enhancement/rgb.png'}


@app.route('/low_light_nir_img', methods=['POST'])
def low_light_nir_img():
    img = request.files.get('file')
    if img is not None:
        img.save('static/low_light_enhancement/nir.png')
    return {'code': 200, 'nir': 'http://127.0.0.1:5590/static/low_light_enhancement/nir.png'}


@app.route('/original_crop_img', methods=['POST'])
def get_ori_crop_img():
    img = request.files.get('file')
    path = 'static/' + request.values['type'] + '/' + 'original_crop.png'
    if img is not None:
        img.save(path)
    return {'code': 200, 'crop_img': 'http://127.0.0.1:5590/' + path}


@app.route('/enhance_crop_img', methods=['POST'])
def get_en_crop_img():
    img = request.files.get('file')
    path = 'static/' + request.values['type'] + '/' + 'enhance_crop.png'
    if img is not None:
        img.save(path)
    return {'code': 200, 'crop_img': 'http://127.0.0.1:5590/' + path}
