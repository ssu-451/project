#!/usr/bin/python3

"""An executable to control the service's behaviour:
check status, start, stop or restart"""

import argparse
import sys
import os
import time
import subprocess
import tqdm

SERVICE_COMMAND = ('gunicorn -D '
                   '--worker-class eventlet '
                   '-b 127.0.0.1:8001 '
                   '--access-logfile access.log '
                   '--log-file error.log '
                   '-p service.pid '
                   'main:APP')


def status(args):
    """A function to handle status queries"""
    if not os.path.exists('service.pid'):
        open('service.pid', 'w').close()
    with open('service.pid') as file:
        pid = file.read()
    pid = pid.replace('\n', '')
    if not pid:
        return False
    command = 'ps ux|grep -v grep|grep {0}|grep "{1}"'.format(
        pid, SERVICE_COMMAND)
    ps_output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) \
        .stdout.read().decode('utf8')
    if args.ps and not args.quiet:
        print('Extract from "ps ux" command output:\n{0}'.format(ps_output))
    return bool(ps_output)


def start(args):
    """A function to handle start queries"""
    if not args.quiet:
        print('Starting service...')
    subprocess.Popen(SERVICE_COMMAND, shell=True).communicate()


def stop(args, kill=False):
    """A function to handle stop queries"""
    with open('service.pid') as file:
        pid = file.read()
    if not args.quiet:
        print('Stopping service...')
    subprocess.Popen('kill {0}{1}'.format(
        '-9 ' if kill else '', pid), shell=True).communicate()


def status_human(args):
    """A function to handle status queries
    with human-readable output"""
    if not args.quiet:
        print('Service is {0}running'.format('' if status(args) else 'not '))


def wait(args):
    """A functin which makes a 5 seconds delay with a progress bar"""
    pbar = None
    if not args.quiet:
        pbar = tqdm.tqdm(total=50)
    for _ in range(50):
        time.sleep(.1)
        if not args.quiet:
            pbar.update()


def file_extract(file_path, offset):
    """A function which returns contents of the file from offset to the end"""
    with open(file_path) as file:
        file.seek(offset)
        extract = file.read()
        if extract:
            return extract
        return '<No lines have been added to the file>'


def start_human(args):
    """A function to handle start queries
    with human-readable output"""
    if status(args):
        if not args.quiet:
            print('Service is already running')
        return
    if not os.path.exists('access.log'):
        open('access.log', 'w').close()
    access_log_size = os.stat('access.log').st_size
    if not os.path.exists('error.log'):
        open('error.log', 'w').close()
    error_log_size = os.stat('error.log').st_size
    start(args)
    wait(args)
    if not status(args):
        print('''ERROR: could not start the service!!!
    Access log extract for the start attempt:
{0}
    Error log extract for the start attempt:
{1}'''.format(file_extract('access.log', access_log_size),
              file_extract('error.log', error_log_size)))
    else:
        if not args.quiet:
            print('Service has been started')


def restart_human(args):
    """A function to handle restart queries
    with human-readable output"""
    stop_human(args)
    start_human(args)


def stop_human(args):
    """A function to handle stop queries
    with human-readable output"""
    if not status(args):
        if not args.quiet:
            print('Service is already not running')
        return
    stop(args)
    wait(args)
    if status(args):
        if not args.quiet:
            print('''ERROR: could not stop the service!!!
Trying SIGKILL...''')
        stop(args, True)
        wait(args)
        if status(args) and not args.quiet:
            print('Could not stop the service even with SIGKILL...')
    if not status(args) and not args.quiet:
        print('Service has been stopped')


def main():
    """The main function"""
    parser = argparse.ArgumentParser(
        description='A script to control a service')
    parser.add_argument('command',
                        help='Command to execute',
                        choices=['status', 'start', 'restart', 'stop'])
    parser.add_argument('--ps',
                        help='Show "ps ux" command output on status queries',
                        action='store_true')
    parser.add_argument('-k', '--kill',
                        help=('Use SIGKILL instead of SIGTERM '
                              'when stopping the service'),
                        action='store_true')
    parser.add_argument('-q', '--quiet',
                        help='No output, except for errors',
                        action='store_true')
    args = parser.parse_args()
    getattr(sys.modules[__name__], args.command + '_human')(args)


if __name__ == '__main__':
    main()
