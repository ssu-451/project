"""
sldkfj
"""
import copy
import math
import random


class NeuralNetwork():
    """
    s
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
        self.shuffle()

    def shuffle(self):
        """
        asd
        """
        for i, _ in enumerate(self.graph):
            for j, _ in enumerate(self.graph[i]):
                for k, _ in enumerate(self.graph[i][j]):
                    self.graph[i][j][k] = random.random() * 3

    def run(self, inputs):
        """
        sds
        """
        for i, _ in enumerate(inputs):
            self.outputs[0][i] = inputs[i]

        for i in range(1, len(self.layer_size)):
            for j in range(self.layer_size[i]):
                self.outputs[i][j] = 0
                for k in range(self.layer_size[i - 1]):
                    self.outputs[i][j] += (self.outputs[i - 1][k] *
                                           self.graph[i - 1][k][j])
                self.outputs[i][j] = self.sigmoid(self.outputs[i][j])

        return self.outputs[-1][0]

    @staticmethod
    def sigmoid(value):
        """
        skdj
        """
        return 1 / (1 + math.exp(-value))

    @classmethod
    def differential(cls, value):
        """
        sd
        """
        sigm = cls.sigmoid(value)
        return sigm * (1 - sigm)

    def train(self, inputs, expected_result):
        """
        ljsdf
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


def main():
    """
    slkdfj
    """
    network = NeuralNetwork([3, 5, 6, 7, 1], 0.2)

    for i, _ in enumerate(network.graph):
        for j, _ in enumerate(network.graph[i]):
            print('[{}, {}]'.format(i, j))
            for _, _ in enumerate(network.graph[i][j]):
                # print('{:.2f}'.format(network.graph[i][j][k]))
                pass

    for _ in range(1000):
        network.train([0, 0, 0], 0)
        network.train([0, 0, 1], 1)  # 1
        network.train([0, 1, 0], 0)
        network.train([0, 1, 1], 0)  # 1
        network.train([1, 0, 0], 1)  # 1
        network.train([1, 0, 1], 1)  # 1
        network.train([1, 1, 0], 0)
        network.train([1, 1, 1], 1)

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
