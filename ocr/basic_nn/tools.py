"""
The main tools of NN
"""
import os
import ocr.basic_nn.nn
from ocr.settings import (
    ALPHABET,
    BASE_DIR,
    NN_LAYERS,
)


def recognize_symbol(inputs, nn_constr=None, alphabet=None):
    """
    Recognition of the one symbol
    """
    if nn_constr is None:
        nn_constr = NN_LAYERS
    if alphabet is None:
        alphabet = ALPHABET

    network = ocr.basic_nn.nn.NeuralNetwork(nn_constr)
    network.load(os.path.join(BASE_DIR, 'coefficients.json'))
    output = network.run(inputs)
    return alphabet[output]


def training_session(train_data, nn_constr=None, restart=False,
                     repetition=100):
    """
    Allows to train Neural Network
    """
    if nn_constr is None:
        nn_constr = NN_LAYERS
    network = ocr.basic_nn.nn.NeuralNetwork(nn_constr, 0.2)
    if not restart:
        network.load(os.path.join(BASE_DIR, 'coefficients.json'))

        assert len(network.graph) == len(nn_constr)
        for i, _ in enumerate(nn_constr):
            assert len(network.graph[i]) == nn_constr[i]
            for neighbors in network.graph[i]:
                assert len(neighbors) == nn_constr[i + 1]

    for attempt in range(repetition):
        print("Training session [attempt={attempt}]".format(attempt=attempt))
        for i, letter in enumerate(train_data['list']):
            network.train(letter['inputs'], i)

        if attempt % 10 == 0:
            network.dump(os.path.join(BASE_DIR, 'coefficients.json'))
