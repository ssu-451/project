#!/usr/bin/python3

import flask
import random
import time

app = flask.Flask(__name__)
symbols = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"',-.:;? абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'''


@app.route('/', methods=['GET'])
def index():
    return flask.redirect('/static/index.html')


@app.route('/api/v0.1/symbol', methods=['POST'])
def recognise_symbol():
    time.sleep(.5)  # Simulating the delay when processing the symbol
    return flask.jsonify({'result': random.choice(symbols)})


if __name__ == '__main__':
    app.run('0.0.0.0', 8001)

