"""
Neural network
"""
import copy
import math
import random


class NeuralNetwork():
    """
    The class which emulates neural network
    """
    def __init__(self, dimension, rate=0.1):
        self.layer_size = dimension
        self.learning_rate = rate

        self.outputs = [[0 for _ in range(size)]
                        for _, size in enumerate(self.layer_size)]
        self.delta = copy.deepcopy(self.outputs)

        self.graph = [[[0 for _ in range(self.layer_size[i + 1])]
                       for j in range(self.layer_size[i])]
                      for i in range(len(self.layer_size) - 1)]

        self.bias = [[0 for _ in range(self.layer_size[i + 1])]
                     for i in range(len(self.layer_size) - 1)]

        self.shuffle()

    def shuffle(self):
        """
        Set random weights
        """
        for i, _ in enumerate(self.graph):
            for j, _ in enumerate(self.graph[i]):
                for k, _ in enumerate(self.graph[i][j]):
                    self.graph[i][j][k] = random.random() * 3

        for i, _ in enumerate(self.bias):
            for j, _ in enumerate(self.bias[i]):
                self.bias[i][j] = random.random() * 3

    def run(self, inputs, need_values=False):
        """
        Get actual result
        """
        for i, _ in enumerate(inputs):
            self.outputs[0][i] = inputs[i]

        for i in range(1, len(self.layer_size)):
            for j in range(self.layer_size[i]):
                self.outputs[i][j] = 0
                for k in range(self.layer_size[i - 1]):
                    self.outputs[i][j] += (self.outputs[i - 1][k] *
                                           self.graph[i - 1][k][j])
                self.outputs[i][j] += self.bias[i - 1][j]
                self.outputs[i][j] = self.sigmoid(self.outputs[i][j])

        if need_values:
            return self.outputs[-1]

        max_val, idx_max = max((val, idx) for idx, val in
                               enumerate(self.outputs[-1]))
        return idx_max

    @staticmethod
    def sigmoid(value):
        """
        Usual sigmoid
        """
        return 1 / (1 + math.exp(-value))

    def differential(self, value):
        """
        Derivation of the sigmoid
        """
        sigm = self.sigmoid(value)
        return sigm * (1 - sigm)

    def train(self, inputs, expected_result):
        """
        Allows to teach NN with input data and expected result
        """
        act_values = self.run(inputs, need_values=True)
        for i, _ in enumerate(act_values):
            exp_val = float(i == expected_result)
            self.delta[-1][i] = ((exp_val - act_values[i]) *
                                  self.differential(act_values[i]))
                                  
        for i in range(len(self.layer_size) - 2, -1, -1):
            for j in range(self.layer_size[i]):
                self.delta[i][j] = 0
                for k in range(self.layer_size[i + 1]):
                    self.graph[i][j][k] += (self.outputs[i][j] *
                                            self.delta[i + 1][k] *
                                            self.learning_rate)
                    self.delta[i][j] += (self.delta[i + 1][k] *
                                         self.graph[i][j][k])
                self.delta[i][j] *= self.differential(self.outputs[i][j])

            for j in range(self.layer_size[i + 1]):
                self.bias[i][j] += (1 * self.delta[i + 1][j] *
                                    self.learning_rate)


if __name__ == '__main__':
    nn = NeuralNetwork([3, 4, 3])
    for _ in range(10000):
        nn.train([0, 1, 1], 1)
        nn.train([1, 0, 1], 0)

    print(nn.run([0, 1, 1], need_values=False))
    print(nn.run([1, 0, 1], need_values=False))
