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
    def __init__(self, dimension=None, rate=0.1):
        if dimension is None:
            dimension = [1, 1]
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

    def run(self, inputs):
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
                # self.outputs[i][j] += self.bias[i - 1][j]
                self.outputs[i][j] = self.sigmoid(self.outputs[i][j])

        return self.outputs[-1][0]

    @staticmethod
    def sigmoid(value):
        """
        Usual sigmoid
        
        try:
            a = 1 / (1 + math.exp(-value))
        except:
            print('fucked up! value:', value)
            print(self.graph)
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
        actual_result = self.run(inputs)
        self.delta[-1][0] = ((expected_result - actual_result) *
                             self.differential(actual_result))
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


def main():
    """
    The main function of the application
    """
    # network = NeuralNetwork([3, 7, 6, 5, 1], 0.2)
    # network = NeuralNetwork([3, 3, 1], 0.2)
    network = NeuralNetwork([3, 20, 1], 0.2)

    for i, _ in enumerate(network.graph):
        for j, _ in enumerate(network.graph[i]):
            #print('[{}, {}]'.format(i, j))
            for _, _ in enumerate(network.graph[i][j]):
                # print('{:.2f}'.format(network.graph[i][j][k]))
                pass

    # print(network.graph)

    for _ in range(1000):
        network.train([0, 0, 0], 0)
        network.train([0, 0, 1], 1)  # 1 # 1
        network.train([0, 1, 0], 0)
        network.train([0, 1, 1], 0)  # 1
        network.train([1, 0, 0], 1)  # 1 # 1
        network.train([1, 0, 1], 1)  # 1 # 1
        network.train([1, 1, 0], 0)
        network.train([1, 1, 1], 1)      # 1

    print(network.run([0, 0, 0]))
    print(network.run([0, 0, 1]))
    print(network.run([0, 1, 0]))
    print(network.run([0, 1, 1]))
    print(network.run([1, 0, 0]))
    print(network.run([1, 0, 1]))
    print(network.run([1, 1, 0]))
    print(network.run([1, 1, 1]))


if __name__ == '__main__':
    main()
