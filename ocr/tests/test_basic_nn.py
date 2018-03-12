"""
Unit tests for the simpliest neural network
"""

import unittest
import ocr.basic_nn.nn


class BasicNnTestCase(unittest.TestCase):
    """
    Service class unittest's library
    """
    ACCURACY = 0.1

    def test_small_nn(self):
        """
        Test for the small NN
        """
        for _ in range(10):
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

    def is_valid_result(self, network, inputs, expected_result):
        """
        Checks if answer is equal to expected_result and
        accuracy is high enough at the same time
        """
        answer, act_values = network.run(inputs, need_values=True)
        print(act_values)
        return (answer == expected_result and
                act_values[answer] > 1 - self.ACCURACY)
