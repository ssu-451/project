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
    for l in lines:
        words = get_words(l)
        for w in words:
            symbols.append(get_symbols(w))
    return symbols


def get_lines(gs_img):
    """This method takes the image of text(PIL.Image object)
    as an argument and return an array of text lines images (PIL.Image object).
    This method is used by get_symbols_from_image method to split
    text image into text lines images"""
    pix = np.array(gs_img, dtype=int)
    height = pix.shape[0]
    width = pix.shape[1]
    sj = pix.sum(axis=1) / width
    sb = st = 254
    is_begin = 0
    line = [0, 0]
    part = []
    n = height - 3
    j = 2
    while j < n:

        if sj[j] < st and sj[j - 1] > st and sj[j - 2] > st and\
                        sj[j + 1] < sb and sj[j + 2] < sb and sj[j + 3] < sb:
            is_begin = 1
            line[0] = j
            j += 1
        if is_begin:
            if (sj[j] < st and sj[j + 1] > sb) or \
                    (sj[j + 1] > sb and sj[j + 2] > sb and sj[j + 3] > sb):
                is_begin = 0
                line[1] = j
                part.append(line)
                line = [0, 0]
        j += 1

    lines = []
    for line in part:
        a = gs_img.crop((0, line[0], width, line[1]))
        lines.append(a)
    return lines


def get_words(line_img):
    """This method takes the image of text line (PIL.Image object)
    as an argument and return an array of words images (PIL.Image object).
    This method is used by get_symbols_from_image method to
    split text line image into words images"""
    pix = np.array(line_img, dtype=int)
    height = pix.shape[0]
    width = pix.shape[1]

    def fx(t):
        return 0 if t < 210 else 255

    fx = np.vectorize(fx)
    pix = fx(pix)

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

    ci = pix.sum(axis=0) / height
    cr = cl = 255
    is_begin = False
    word = [0, 0]
    part = []
    m = width - 4
    i = 1
    while i < m:
        if not is_begin and ci[i] < cl and ci[i + 1] < cl and ci[i - 1] >= cl:
            is_begin = True
            word[0] = i
            i += 1
        if is_begin:
            if ci[i] >= cr and ci[i + 1] >= cr and ci[i + 2] >= cr and\
                            ci[i - 1] < cr and ci[i - 2] < cr:
                is_begin = False
                word[1] = i
                part.append(word)
                word = [0, 0]
        i += 1

    words = []
    for word in part:
        a = line_img.crop((word[0], 0, word[1], height))
        words.append(a)
    return words


def get_symbols(word_img):
    """This method the image of word (PIL.Image object)
     as an argument and return an array of symbols images,  (PIL.Image object).
     This method is used by get_symbols_from_image method to split the image
      of word into symbols images"""
    pix = np.array(word_img, dtype=int)
    height = pix.shape[0]
    width = pix.shape[1]
    ci = pix.sum(axis=0) / height
    kb = ci.sum() / width

    cmax = pix.max(axis=0)
    cb = kb * 1.05

    df = int(0.3 * height)
    dmin = int(0.4 * height)

    w0 = []
    left = 0
    r = left + df
    while r < width:
        max = left + np.argmax(ci[left:r])
        w0.append(max)
        left = max + 1
        r = left + df

    w1 = []
    for l in w0:
        if ci[l] > cb:
            w1.append(l)

    p1 = int(height * 0.3)
    p2 = p1 + int(height * 0.4)

    bh = pix[:p1].argmin(axis=0)
    bm = pix[p1:p2].argmin(axis=0)
    bl = pix[p2:height].argmin(axis=0)

    w2 = []
    i = 0
    n = len(w1)
    while i < n:
        ind = w1[i]
        cl2 = (ci[ind - 1] > cmax[ind]
               and cmax[ind - 1] < 2 * math.fabs(cmax[ind - 1] - cmax[ind]))
        cr2 = (ci[ind] > cmax[ind + 1]
               and cmax[ind] < 2 * math.fabs(cmax[ind] - cmax[ind + 1]))
        cl = (bh[ind] == bh[ind - 1] or bm[ind] == bm[ind - 1]
              or bl[ind] == bl[ind - 1]) and cl2
        cr = (bh[ind] == bh[ind + 1] or bm[ind] == bm[ind + 1]
              or bl[ind] == bl[ind + 1]) and cr2
        if not (cl and cr):
            w2.append(w1[i])
        i += 1

    i = 1
    while i < len(w2):
        if w2[i] - w2[i - 1] < dmin:
            w2.remove(w2[i])
        else:
            i += 1

    symbols = []
    n = len(w2)

    i = 1
    while i < n:
        left = w2[i - 1]
        r = w2[i]
        a = word_img.crop((left, 0, r, height))
        symbols.append(a)
        i += 1
    return symbols
