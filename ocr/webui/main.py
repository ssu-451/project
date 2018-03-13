#!/usr/bin/python3

"""A module for flask web interface"""

import random
import time
import flask

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
    return flask.jsonify({'result': random.choice(SYMBOLS)})


if __name__ == '__main__':
    APP.run('0.0.0.0', 8001)
