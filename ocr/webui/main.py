#!/usr/bin/python3

"""A module for flask web interface"""

import random
import time
import flask
import re
import io
import PIL.Image
import base64
import ocr.utilities.get_pixels
import ocr.basic_nn.tools


APP = flask.Flask(__name__)
SYMBOLS = ('''0123456789abcdefghijklmn'''
           '''opqrstuvwxyzABCDEFGHIJKL'''
           '''MNOPQRSTUVWXYZ!"',-.:;? '''
           '''абвгдеёжзийклмнопрстуфхц'''
           '''чшщъыьэюяАБВГДЕЁЖЗИЙКЛМН'''
           '''ОПРСТУФХЦЧШЩЪЫЬЭЮЯ''')


@APP.route('/', methods=['GET'])
def index():
    """A function handling / requests, returns the webpage for one symbol"""
    return flask.redirect('/static/index.html')


@APP.route('/api/v0.1/symbol', methods=['POST'])
def recognise_symbol():
    """A function handling API recognise symbol requests"""
    time.sleep(.5)  # Simulating the delay when processing the symbol
    image_data = re.sub('^data:image/.+;base64,', '', flask.request.form['file'])
    image = PIL.Image.open(io.BytesIO(base64.b64decode(image_data)))
    image = image.resize((16, 16), PIL.Image.LANCZOS)
    pixels = ocr.utilities.get_pixels.get_pixels(image).flatten()
    pixels = [1 - pixel for pixel in pixels]
    print(pixels)
    return flask.jsonify({'result': ocr.basic_nn.tools.recognize_symbol(pixels)})


if __name__ == '__main__':
    APP.run('0.0.0.0', 8001)
