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
            network = ocr.basic_nn.nn.NeuralNetwork([3, 3, 1], 0.2)
            for _ in range(10000):
                network.train([0, 0, 0], 0)
                network.train([0, 0, 1], 1)  # 1 # 1
                network.train([0, 1, 0], 0)
                network.train([0, 1, 1], 0)  # 1
                network.train([1, 0, 0], 1)  # 1 # 1
                network.train([1, 0, 1], 1)  # 1 # 1
                network.train([1, 1, 0], 0)
                network.train([1, 1, 1], 1)      # 1

            self.assertTrue(network.run([0, 0, 0]) < self.ACCURACY)
            self.assertTrue(network.run([0, 0, 1]) > 1 - self.ACCURACY)
            self.assertTrue(network.run([0, 1, 0]) < self.ACCURACY)
            self.assertTrue(network.run([0, 1, 1]) < self.ACCURACY)
            self.assertTrue(network.run([1, 0, 0]) > 1 - self.ACCURACY)
            self.assertTrue(network.run([1, 0, 1]) > 1 - self.ACCURACY)
            self.assertTrue(network.run([1, 1, 0]) < self.ACCURACY)
            self.assertTrue(network.run([1, 1, 1]) > 1 - self.ACCURACY)
