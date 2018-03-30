#!/usr/bin/python3

"""This executable tests the neural network on all symbols
specified in training_set.json and prints the percentage of
correct NN's answers"""

import os
import json
import ocr.settings
import ocr.basic_nn.tools

REPETITIONS = 5


def correct_fraction():
    """A function which prints and returns the fraction of
    correct answers of the NN among the total number of letters"""
    with open(os.path.join(ocr.settings.BASE_DIR,
                           'training_set.json')) as file:
        training_set = json.load(file)
    correct = 0
    for letter in training_set['list']:
        print(letter['letter'])
        for _ in range(REPETITIONS):
            if ocr.basic_nn.tools.recognize_symbol(letter['inputs']) \
              == letter['letter']:
                correct += 1 / REPETITIONS
    fraction = correct / len(training_set['list'])
    print(fraction)
    return fraction


def main():
    """The main function"""
    print('{0}% correct'.format(100 * correct_fraction()))


if __name__ == '__main__':
    main()
