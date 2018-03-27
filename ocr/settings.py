"""
Project settings
"""
import os

ALPHABET = (" !?\"',-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            "abcdefghijklmnopqrstuvwxyz")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NN_LAYERS = [16*16, 150, 70]
