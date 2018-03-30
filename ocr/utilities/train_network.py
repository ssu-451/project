"""
Train network
"""
import json
import os
import sys
from ocr.basic_nn.tools import training_session
from ocr.settings import BASE_DIR, NN_LAYERS

REPETITION = 1000


def main(repetition=REPETITION):
    """
    The main function of the module
    """
    train_data = json.load(open(
        os.path.join(BASE_DIR, 'training_set.json')))
    assert train_data['size'] == NN_LAYERS[2]
    for _, elem in enumerate(train_data['list']):
        assert len(elem['inputs']) == NN_LAYERS[0]

    if len(sys.argv) == 2 and sys.argv[1] == 'restart':
        training_session(train_data, NN_LAYERS, restart=True, repetition=repetition)
    else:
        training_session(train_data, NN_LAYERS, repetition=repetition)


if __name__ == '__main__':
    main()
