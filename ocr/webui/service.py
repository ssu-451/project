#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import subprocess
import time
import os
import tqdm

SERVICE_COMMAND = 'gunicorn -D ' \
                  '--worker-class eventlet ' \
                  '-b 127.0.0.1:8001 ' \
                  '--access-logfile access.log ' \
                  '--log-file error.log ' \
                  'main:app'
SERVICE_SHORT_NAME = '127.0.0.1:8001'


def status(showPs=False):
    psOutput = subprocess.Popen('ps ux|grep -v grep|grep "{0}"'.format(SERVICE_SHORT_NAME), shell=True,
                                stdout=subprocess.PIPE).stdout.read().decode('utf8')
    if showPs:
        print('Extract from "ps ux" command output:')
        print(psOutput)
    return bool(psOutput)


def start():
    print('Starting service...')
    subprocess.Popen(SERVICE_COMMAND, shell=True).communicate()
    print('Waiting for the service to boot up...')
    for _ in tqdm.tqdm(range(50)):
        time.sleep(0.1)


def stop(kill=False):
    print('Stopping service...')
    subprocess.Popen('pkill{1} -f "{0}"'.format(SERVICE_SHORT_NAME, ' -9' if kill else ''), shell=True).communicate()
    print('Waiting for the service to shutdown...')
    for _ in tqdm.tqdm(range(50)):
        time.sleep(0.1)


def printFileExtract(filePath, offset):
    file = open(filePath)
    file.seek(offset)
    extract = file.read()
    if extract:
        print(extract)
    else:
        print('<No lines have been added to the file>')
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A script to control the web service')
    parser.add_argument('command', help='Command to execute', choices=['status', 'start', 'restart', 'stop'])
    parser.add_argument('--ps', help='Show "ps ux" command output on status queries', action='store_true')
    parser.add_argument('-k', '--kill', help='Use SIGKILL instead of SIGTERM when stopping the service',
                        action='store_true')
    args = parser.parse_args()
    command = args.command
    if not os.path.exists('access.log'):
        open('access.log', 'w').close()
    accessLogSize = os.stat('access.log').st_size
    if not os.path.exists('error.log'):
        open('error.log', 'w').close()
    errorLogSize = os.stat('error.log').st_size
    if command == 'status':
        print('Service is {0}running'.format('' if status(args.ps) else 'not '))
    elif command == 'start':
        if status(args.ps):
            print('Service is already running')
        else:
            start()
            if not status(args.ps):  # If it didn't work
                print('ERROR: could not start the service!!!')
                print('    Access log extract for the start attempt:')
                printFileExtract('access.log', accessLogSize)
                print('    Error log extract for the start attempt:')
                printFileExtract('error.log', errorLogSize)
            else:  # If it did work
                print('Service has been started')
    elif command == 'restart':
        subprocess.Popen('./service.py stop{0}{1}'.format(' --ps' if args.ps else '', ' -k' if args.kill else ''),
                         shell=True,
                         stdout=sys.stdout).communicate()
        subprocess.Popen('./service.py start{0}'.format(' --ps' if args.ps else ''), shell=True,
                         stdout=sys.stdout).communicate()
    elif command == 'stop':
        if not status(args.ps):
            print('Service is already not running')
        else:
            stop(args.kill)
            if status(args.ps):  # If it didn't work
                print('ERROR: could not stop the service!!!')
                if not args.kill:  # If SIGKILL was not used
                    if input('Would you like to send SIGKILL to it? (y/n) ').lower() == 'y':
                        subprocess.Popen('./service.py stop -k', shell=True, stdout=sys.stdout).communicate()
                else:  # If it was used
                    print('Could not stop the service even with SIGKILL...')
            else:  # If it did work
                print('Service has been stopped')
