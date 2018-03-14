#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""An executable to control the service's behaviour:
check status, start, stop or restart"""

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
                  'main:APP'
SERVICE_SHORT_NAME = '127.0.0.1:8001'


def status(show_ps=False):
    """A function which returns the status of the service: working or not"""
    ps_output = subprocess.Popen('ps ux|grep -v grep|grep "{0}"'.format(
        SERVICE_SHORT_NAME),
                                 shell=True,
                                 stdout=subprocess.PIPE
                                ).stdout.read().decode('utf8')
    if show_ps:
        print('Extract from "ps ux" command output:')
        print(ps_output)
    return bool(ps_output)


def start():
    """A function which starts the service"""
    print('Starting service...')
    subprocess.Popen(SERVICE_COMMAND, shell=True).communicate()
    print('Waiting for the service to boot up...')
    for _ in tqdm.tqdm(range(50)):
        time.sleep(0.1)


def stop(kill=False):
    """A function which stops the service"""
    print('Stopping service...')
    subprocess.Popen('pkill{1} -f "{0}"'.format(
        SERVICE_SHORT_NAME, ' -9' if kill else ''),
                     shell=True).communicate()
    print('Waiting for the service to shutdown...')
    for _ in tqdm.tqdm(range(50)):
        time.sleep(0.1)


def print_file_extract(file_path, offset):
    """A function which prints contents of the file from offset to the end"""
    file = open(file_path)
    file.seek(offset)
    extract = file.read()
    if extract:
        print(extract)
    else:
        print('<No lines have been added to the file>')
    file.close()


def status_output(args):
    """A function which prints the status of the service
    in a human-readable way"""
    print('Service is {0}running'.format('' if status(args.ps) else 'not '))


def start_output(args):
    """A function which starts the service with human-readable output"""

    if not os.path.exists('access.log'):
        open('access.log', 'w').close()
    access_log_size = os.stat('access.log').st_size
    if not os.path.exists('error.log'):
        open('error.log', 'w').close()
    error_log_size = os.stat('error.log').st_size

    if status(args.ps):
        print('Service is already running')
    else:
        start()
        if not status(args.ps):  # If it didn't work
            print('ERROR: could not start the service!!!')
            print('    Access log extract for the start attempt:')
            print_file_extract('access.log', access_log_size)
            print('    Error log extract for the start attempt:')
            print_file_extract('error.log', error_log_size)
        else:  # If it did work
            print('Service has been started')


def restart_output(args):
    """A function which restart the service with human-readable output"""
    subprocess.Popen('./service.py stop{0}{1}'.format(
        ' --ps' if args.ps else '', ' -k' if args.kill else ''),
                     shell=True,
                     stdout=sys.stdout).communicate()
    subprocess.Popen('./service.py start{0}'.format(
        ' --ps' if args.ps else ''), shell=True,
                     stdout=sys.stdout).communicate()


def stop_output(args):
    """A function which stops the service with human-readable output"""
    if not status(args.ps):
        print('Service is already not running')
    else:
        stop(args.kill)
        if status(args.ps):  # If it didn't work
            print('ERROR: could not stop the service!!!')
            if not args.kill:  # If SIGKILL was not used
                if input(('Would you like to send '
                          'SIGKILL to it? (y/n) ')).lower() == 'y':
                    subprocess.Popen('./service.py stop -k',
                                     shell=True,
                                     stdout=sys.stdout).communicate()
            else:  # If it was used
                print('Could not stop the service even with SIGKILL...')
        else:  # If it did work
            print('Service has been stopped')


def main():
    """The main function"""
    parser = argparse.ArgumentParser(
        description='A script to control the web service')
    parser.add_argument('command',
                        help='Command to execute',
                        choices=['status', 'start', 'restart', 'stop'])
    parser.add_argument('--ps',
                        help='Show "ps ux" command output on status queries',
                        action='store_true')
    parser.add_argument('-k',
                        '--kill',
                        help=('Use SIGKILL instead of SIGTERM '
                              'when stopping the service'),
                        action='store_true')
    args = parser.parse_args()
    command = args.command
    getattr(sys.modules[__name__], command + '_output')(args)


if __name__ == '__main__':
    main()
