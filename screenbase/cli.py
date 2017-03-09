"""
CLI entrypoint module
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging
from argparse import ArgumentParser
from getpass import getuser
from os import path
from time import sleep

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

from .watchers import ScreenshotWatcher

DEFAULT_DIR = path.expanduser('~/Desktop')
DEFAULT_USER = getuser()


def _get_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-u',
        '--user',
        metavar='USER',
        help='Your keybase.io username',
        default=DEFAULT_USER)
    parser.add_argument(
        '-d',
        '--directory',
        metavar='WATCHDIR',
        help='Directory to watch for new screenshots',
        default=DEFAULT_DIR)
    parser.add_argument(
        '-v',
        '--verbose',
        help='Directory to watch for new screenshots',
        action='store_true',
        default=DEFAULT_DIR)

    return parser.parse_args()


def run():
    """
    Run the CLI tool
    """

    args = _get_args()
    observer = Observer()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    if args.verbose is True:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging_handler = LoggingEventHandler()
        observer.schedule(logging_handler, args.directory, recursive=False)

    logging.info('Using keybase.io user %s', args.user)
    logging.info('Watching %s for screenshot events', args.directory)

    observer.schedule(ScreenshotWatcher(args), args.directory, recursive=False)

    observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
