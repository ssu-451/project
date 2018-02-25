#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This module will contain helper methods utilized by neural network"""

from PIL import Image
import numpy as np


def get_pixels(path):
    """This method takes path to the image as an argument
    convert it to bi-level format and return two dimensional array of 0,1
    where 0 - black 1 - white"""
    img = Image.open(path)
    bw_img = img.convert('1')
    pix = np.array(bw_img, dtype=int)
    return pix
