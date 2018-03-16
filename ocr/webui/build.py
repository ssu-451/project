#!/usr/bin/python3

import requests
import json
import subprocess

with open('telegram.json') as file:
    telegram_config = json.load(file)


def notify(message):
    message = 'Jenkins OCR build:\n{0}'.format(message)
    requests.get('https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format(
        telegram_config['token'], telegram_config['chat_id'], message))


def main():
    output = subprocess.Popen('python3 service.py restart -q',
                              shell=True,
                              stdout=subprocess.PIPE).stdout.read().decode('utf8')
    if output:
        notify(output)


if __name__ == '__main__':
    main()
