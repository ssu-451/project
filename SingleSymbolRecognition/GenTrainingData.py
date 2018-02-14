#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import re
import tqdm
import selenium.webdriver
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force regenerate existing images')
    args = parser.parse_args()
    if not args.force:
        print('Launch this executable with -h parameter for help')
    with open('symbols.txt') as f:
        symbols = f.read()
    with open('fonts.txt') as f:
        fonts = f.read().split('\n')
    with open('resolutions.txt') as f:
        resolutions = f.read().split('\n')
    if not os.path.exists('TrainingData'):
        os.mkdir('TrainingData')
    resolutionPattern = re.compile(r'(\d+)x(\d+)')
    pBar = tqdm.tqdm(total=len(resolutions) * len(fonts) * len(symbols))
    for resolution in resolutions:
        match = resolutionPattern.match(resolution)
        if match is None:
            pBar.update(len(fonts) * len(symbols))
            continue
        driver = selenium.webdriver.PhantomJS()
        driver.set_window_size(int(match.group(1)), int(match.group(2)))
        driver.get('test.html')
        for font in fonts:
            driver.execute_script('$("div").css("font-family", "{0}");'.format(font))
            # driver.execute_script('''''')
            for symbol in symbols:
                if symbol in ['\n', '\t', '\r']:
                    pBar.update()
                    continue
                imageName = 'TrainingData/R{res}|F{font}|S{symbol}.png'.format(res=resolution, font=font, symbol=symbol)
                if os.path.exists(imageName) and not args.force:
                    pBar.update()
                    continue
                script = '$("div").html({0});'.format(
                    '"{0}"'.format(symbol) if symbol != '"' else "'{0}'".format(symbol))
                driver.execute_script(script)
                driver.save_screenshot(imageName)
                pBar.update()
