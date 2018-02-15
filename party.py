"""
Introduction to neural networks
"""
import math


LEARNING_RATE = 0.2


def sigmoid(arg):
    """
    Standart function for sigmoid calculation
    """
    return 1 / (1 + math.exp(-arg))


def train(x_layer, hid_layer, x_data, exp_res):
    """
    The function is used for clarification of NN's coefficients
    """
    hid_layer['val'] = [0, 0]
    for i, x_arr in enumerate(x_layer['weight']):
        for j, weight in enumerate(x_arr):
            hid_layer['val'][j] += x_data[i] * weight
    hid_layer['val'] = list(map(sigmoid, hid_layer['val']))

    y_layer = {
        'val': 0,
    }
    for i, _ in enumerate(hid_layer['val']):
        y_layer['val'] += hid_layer['val'][i] * hid_layer['weight'][i]
    y_layer['val'] = sigmoid(y_layer['val'])

    y_layer['delta'] = exp_res - y_layer['val']
    hid_layer['delta'] = list(map(lambda x: x * y_layer['delta'],
                                  hid_layer['weight']))
    y_diff = sigmoid(y_layer['val']) * (1 - sigmoid(y_layer['val']))

    for i, _ in enumerate(hid_layer['weight']):
        hid_layer['weight'][i] += (
            hid_layer['val'][i] * hid_layer['delta'][i] *
            y_diff * LEARNING_RATE)

    x_layer['delta'] = [0, 0, 0]
    for i, x_arr in enumerate(x_layer['weight']):
        for j, weight in enumerate(x_arr):
            x_layer['delta'][i] += hid_layer['delta'][j] * weight

    hid_layer['diff'] = list(map(lambda x: sigmoid(x) * (1 - sigmoid(x)),
                                 hid_layer['val']))
    for i, x_arr in enumerate(x_layer['weight']):
        for j, weight in enumerate(x_arr):
            x_arr[j] += (x_data[i] * x_layer['delta'][i] *
                         hid_layer['diff'][j] * LEARNING_RATE)


def main():
    """
    The main function of the application
    """
    x_layer = {
        'weight': [[0.5, 0.5], [0.5, 0.5], [0.5, 0.5]],
    }
    hid_layer = {
        'weight': [0.5, 0.5],
    }
    train(x_layer, hid_layer, [1, 0, 0], 1)


if __name__ == '__main__':
    main()
