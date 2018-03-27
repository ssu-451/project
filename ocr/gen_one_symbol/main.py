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


def generate():
    """The main function, which does the generation, hence the name :)"""

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force regenerate existing images')
    args = parser.parse_args()
    if not args.force:
        print('Launch this executable with -h parameter for help')
    with open('symbols.txt') as file:
        symbols = file.read()
    with open('fonts.txt') as file:
        fonts = [font for font in file.read().split('\n') if font]
    with open('resolutions.txt') as file:
        resolutions = file.read().split('\n')
    if not os.path.exists('training_data'):
        os.mkdir('training_data')
    resolution_pattern = re.compile(r'(\d+)x(\d+)')
    pbar = tqdm.tqdm(total=len(resolutions) * len(fonts) * len(symbols))
    for resolution in resolutions:
        match = resolution_pattern.match(resolution)
        if match is None:
            pbar.update(len(fonts) * len(symbols))
            continue
        driver = selenium.webdriver.PhantomJS()
        driver.set_window_size(int(match.group(1)), int(match.group(2)))
        driver.get('test.html')
        for font in fonts:
            driver.execute_script(
                '$("div").css("font-family", "{0}");'.format(font))
            # driver.execute_script('''''')
            for symbol in symbols:
                if symbol in ['\n', '\t', '\r']:
                    pbar.update()
                    continue
                image_name = ('training_data/'
                              'R{res}|F{font}|S{symbol}.png').format(
                                  res=resolution, font=font, symbol=symbol)
                if os.path.exists(image_name) and not args.force:
                    pbar.update()
                    continue
                script = '$("div").html({0});'.format(
                    '"{0}"'.format(
                        symbol) if symbol != '"' else "'{0}'".format(symbol))
                driver.execute_script(script)
                driver.save_screenshot(image_name)
                pbar.update()


if __name__ == '__main__':
    generate()
