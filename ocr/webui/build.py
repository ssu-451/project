#!/usr/bin/python3

"""An executable which is supposed to be called by Jenkins
after updating the working dir to the github repository
Launches the web service and reports all errors to Telegram"""

import json
import subprocess
import requests

with open('telegram.json') as file:
    TELEGRAM_CONFIG = json.load(file)


def notify(message):
    """A function which sends the message to Telegram with a header"""
    message = 'Jenkins OCR build:\n{0}'.format(message)
    requests.get(('https://api.telegram.org/bot{0}'
                  '/sendMessage?chat_id={1}&text={2}').format(
                      TELEGRAM_CONFIG['token'],
                      TELEGRAM_CONFIG['chat_id'],
                      message))


def main():
    """The main function"""
    output = subprocess.Popen('python3 service.py restart -q',
                              shell=True,
                              stdout=subprocess.PIPE) \
        .stdout.read().decode('utf8')
    if output:
        notify(output)


if __name__ == '__main__':
    main()
