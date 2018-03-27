"""
Unit tests for the simpliest neural network
"""

import json
import os
import unittest

import ocr.basic_nn.nn
from ocr.settings import BASE_DIR
from ocr.basic_nn import tools


class BasicNnTestCase(unittest.TestCase):
    """
    Service class unittest's library
    """
    ACCURACY = 0.1

    def test_small_nn(self):
        """
        Test case for the small NN
        """
        network = ocr.basic_nn.nn.NeuralNetwork([3, 3, 2], 0.2)
        for _ in range(10000):
            network.train([0, 0, 0], 0)
            network.train([0, 0, 1], 1)
            network.train([0, 1, 0], 0)
            network.train([0, 1, 1], 0)
            network.train([1, 0, 0], 1)
            network.train([1, 0, 1], 1)
            network.train([1, 1, 0], 0)
            network.train([1, 1, 1], 1)

        self.assertTrue(self.is_valid_result(network, [0, 0, 0], 0))
        self.assertTrue(self.is_valid_result(network, [0, 0, 1], 1))
        self.assertTrue(self.is_valid_result(network, [0, 1, 0], 0))
        self.assertTrue(self.is_valid_result(network, [0, 1, 1], 0))
        self.assertTrue(self.is_valid_result(network, [1, 0, 0], 1))
        self.assertTrue(self.is_valid_result(network, [1, 0, 1], 1))
        self.assertTrue(self.is_valid_result(network, [1, 1, 0], 0))
        self.assertTrue(self.is_valid_result(network, [1, 1, 1], 1))

    def test_aye_nn(self):
        """
        Test case for the NN that recognizes only A, Y and E letters
        """
        train_data = json.load(
            open(os.path.join(BASE_DIR,
                              os.path.join('tests', 'nn_aye.json'))))
        network = ocr.basic_nn.nn.NeuralNetwork([16*16, 150, 3], 0.5)

        for _ in range(100):
            for i in range(train_data['size']):
                network.train(train_data['list'][i]['inputs'], i)

        for i in range(train_data['size']):
            self.assertTrue(self.is_valid_result(
                network, train_data['list'][i]['inputs'], i))

    def test_simple_training(self):
        """
        Checks crucial functions of the NN
        """
        nn_constr = [16*16, 150, 3]
        train_data = json.load(
            open(os.path.join(BASE_DIR,
                              os.path.join('tests', 'nn_aye.json'))))
        tools.training_session(train_data, nn_constr, True, 101)
        network = ocr.basic_nn.nn.NeuralNetwork(nn_constr)
        network.load(os.path.join(BASE_DIR, 'coefficients.json'))

        self.assertEqual(
            tools.recognize_symbol(train_data['list'][0]['inputs'],
                                   nn_constr,
                                   'AYE'),
            'A')
        self.assertEqual(
            tools.recognize_symbol(train_data['list'][1]['inputs'],
                                   nn_constr,
                                   'AYE'),
            'Y')
        self.assertEqual(
            tools.recognize_symbol(train_data['list'][2]['inputs'],
                                   nn_constr,
                                   'AYE'),
            'E')

    def is_valid_result(self, network, inputs, expected_result):
        """
        Checks if answer is equal to expected_result and
        accuracy is high enough at the same time
        """
        answer, act_values = network.run(inputs, need_values=True)
        return (answer == expected_result and
                act_values[answer] > 1 - self.ACCURACY)
