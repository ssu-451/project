#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""This executable generates images of single symbols,
listed in symbols.txt file, with fonts, listed in fonts.txt,
using selenium and PhantomJS"""

import argparse
import re
import os
import tqdm
import selenium.webdriver

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-f', '--force', action='store_true',
                        help='Force regenerate existing images')
    ARGS = PARSER.parse_args()
    if not ARGS.force:
        print('Launch this executable with -h parameter for help')
    with open('symbols.txt') as f:
        SYMBOLS = f.read()
    with open('fonts.txt') as f:
        FONTS = [font for font in f.read().split('\n') if font]
    with open('resolutions.txt') as f:
        RESOLUTIONS = f.read().split('\n')
    if not os.path.exists('TrainingData'):
        os.mkdir('TrainingData')
    RESOLUTION_PATTERN = re.compile(r'(\d+)x(\d+)')
    PBAR = tqdm.tqdm(total=len(RESOLUTIONS) * len(FONTS) * len(SYMBOLS))
    for resolution in RESOLUTIONS:
        match = RESOLUTION_PATTERN.match(resolution)
        if match is None:
            PBAR.update(len(FONTS) * len(SYMBOLS))
            continue
        driver = selenium.webdriver.PhantomJS()
        driver.set_window_size(int(match.group(1)), int(match.group(2)))
        driver.get('test.html')
        for font in FONTS:
            driver.execute_script(
                '$("div").css("font-family", "{0}");'.format(font))
            # driver.execute_script('''''')
            for symbol in SYMBOLS:
                if symbol in ['\n', '\t', '\r']:
                    PBAR.update()
                    continue
                imageName = 'TrainingData/R{res}|F{font}|S{symbol}.png'.format(
                    res=resolution,
                    font=font,
                    symbol=symbol)
                if os.path.exists(imageName) and not ARGS.force:
                    PBAR.update()
                    continue
                script = '$("div").html({0});'.format(
                    '"{0}"'.format(
                        symbol) if symbol != '"' else "'{0}'".format(symbol))
                driver.execute_script(script)
                driver.save_screenshot(imageName)
                PBAR.update()
