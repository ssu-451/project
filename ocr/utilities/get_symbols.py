#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This module  contains methods to split text image into symbols"""
import math
from PIL import Image
import numpy as np


def get_symbols_from_image(path):
    """This method takes path to the text image as an argument
    and return an array of words, every word is an array of symbols,
    symbol is a instance of PIL.Image object"""
    img = Image.open(path)
    gs_img = img.convert('L')
    lines = get_lines(gs_img)
    symbols = []
    for line in lines:
        words = get_words(line)
        for word in words:
            symbols.append(get_symbols(word))
    return symbols


def get_lines(gs_img):
    """This method takes the image of text(PIL.Image object)
    as an argument and return an array of text lines images (PIL.Image object).
    This method is used by get_symbols_from_image method to split
    text image into text lines images"""
    pix = np.array(gs_img, dtype=int)
    height = pix.shape[0]
    width = pix.shape[1]
    s_j = pix.sum(axis=1) / width
    s_b = s_t = 254
    is_begin = 0
    line = [0, 0]
    part = []
    j = 2
    while j < height - 3:
        c_1 = (s_j[j] < s_t
               and s_j[j - 1] > s_t
               and s_j[j - 2] > s_t
               and s_j[j + 1] < s_b
               and s_j[j + 2] < s_b
               and s_j[j + 3] < s_b)
        if c_1:
            is_begin = 1
            line[0] = j
            j += 1
        if is_begin:
            c_2 = ((s_j[j] < s_t
                    and s_j[j + 1] > s_b)
                   or (s_j[j + 1] > s_b
                       and s_j[j + 2] > s_b
                       and s_j[j + 3] > s_b))
            if c_2:
                is_begin = 0
                line[1] = j
                part.append(line)
                line = [0, 0]
        j += 1

    lines = []
    for line in part:
        line_img = gs_img.c_rop((0, line[0], width, line[1]))
        lines.append(line_img)
    return lines


def get_words(line_img):
    """This method takes the image of text line (PIL.Image object)
    as an argument and return an array of words images (PIL.Image object).
    This method is used by get_symbols_from_image method to
    split text line image into words images"""
    pix = np.array(line_img, dtype=int)
    height = pix.shape[0]
    width = pix.shape[1]

    def contrast(pix):
        """Contrast image"""
        return 0 if pix < 210 else 255

    contrast = np.vectorize(contrast)
    pix = contrast(pix)

    for i in range(3, height - 3):
        for j in range(3, width - 3):
            if pix[i][j] == 0:
                for k in range(-3, 4):
                    pix[i + k][j] = 1
                    pix[i + k][j + 1] = 1
                    pix[i + k][j + 2] = 1
                    pix[i + k][j - 1] = 1
                    pix[i + k][j - 2] = 1
                    pix[i + k][j - 3] = 1
                    pix[i + k][j + 3] = 1

    c_i = pix.sum(axis=0) / height
    c_r = 255
    is_begin = False
    word = [0, 0]
    part = []
    i = 1
    while i < width - 4:
        if (not is_begin) and c_i[i] < c_r and\
                        c_i[i + 1] < c_r and c_i[i - 1] >= c_r:
            is_begin = True
            word[0] = i
            i += 1
        if is_begin:
            if c_i[i] >= c_r and c_i[i + 1] >= c_r and c_i[i + 2] >= c_r and\
                            c_i[i - 1] < c_r and c_i[i - 2] < c_r:
                is_begin = False
                word[1] = i
                part.append(word)
                word = [0, 0]
        i += 1

    words = []
    for word in part:
        word_img = line_img.c_rop((word[0], 0, word[1], height))
        words.append(word_img)
    return words


def get_symbols(word_img):
    """This method the image of word (PIL.Image object)
     as an argument and return an array of symbols images,  (PIL.Image object).
     This method is used by get_symbols_from_image method to split the image
      of word into symbols images"""
    def get_partitions(c_i, width, d_f, c_b):
        """Return potential symbols partitions"""
        w_0 = []
        left = 0
        right = left + d_f
        while right < width:
            max_ind = left + np.argmax(c_i[left:right])
            w_0.append(max_ind)
            left = max_ind + 1
            right = left + d_f

        w_1 = []
        for part in w_0:
            if c_i[part] > c_b:
                w_1.append(part)
        return w_1

    def remove_spare_partitions(c_i, c_max, w_1, d_min, height):
        """Remove all spare symbols partitions"""
        p_1 = int(height * 0.3)
        p_2 = p_1 + int(height * 0.4)

        b_h = pix[:p_1].argmin(axis=0)
        b_m = pix[p_1:p_2].argmin(axis=0)
        b_l = pix[p_2:height].argmin(axis=0)

        w_2 = []
        for ind in w_1:
            c_l = ((b_h[ind] == b_h[ind - 1]
                    or b_m[ind] == b_m[ind - 1]
                    or b_l[ind] == b_l[ind - 1])
                   and c_i[ind - 1] > c_max[ind]
                   and c_max[ind - 1] < 2 *
                   math.fabs(c_max[ind - 1] - c_max[ind]))
            c_r = ((b_h[ind] == b_h[ind + 1]
                    or b_m[ind] == b_m[ind + 1]
                    or b_l[ind] == b_l[ind + 1])
                   and c_i[ind] > c_max[ind + 1]
                   and c_max[ind] < 2 * math.fabs(c_max[ind] - c_max[ind + 1]))
            if not (c_l and c_r):
                w_2.append(ind)

        i = 1
        while i < len(w_2):
            if w_2[i] - w_2[i - 1] < d_min:
                w_2.remove(w_2[i])
            else:
                i += 1

        return w_2

    pix = np.array(word_img, dtype=int)
    height = pix.shape[0]
    c_i = pix.sum(axis=0) / height
    w_0 = get_partitions(c_i,
                         pix.shape[1],
                         int(0.3 * height),
                         c_i.sum()/pix.shape[1] * 1.05)
    w_1 = remove_spare_partitions(c_i,
                                  pix.max(axis=0),
                                  w_0,
                                  int(0.4 * height),
                                  height)
    symbols = []
    i = 1
    while i < len(w_1):
        left = w_1[i - 1]
        right = w_1[i]
        symb_img = word_img.c_rop((left, 0, right, height))
        symbols.append(symb_img)
        i += 1
    return symbols
