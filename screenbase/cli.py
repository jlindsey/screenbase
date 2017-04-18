#  Copyright (C) 2017 Joshua Lindsey <joshua.s.lindsey@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
CLI entrypoint module
"""

from __future__ import absolute_import, print_function, unicode_literals

import logging
from argparse import ArgumentParser
from collections import namedtuple
from getpass import getuser
from os import path
from time import sleep

from watchdog.events import LoggingEventHandler
from watchdog.observers import Observer

import yaml

from . import __VERSION__
from .watchers import ScreenshotWatcher

DEFAULT_CONFIG_FILE = path.join(path.expanduser('~'), '.config', 'screenbase')
DEFAULT_DIR = path.expanduser('~/Desktop')
DEFAULT_USER = getuser()
DEFAULT_MATCHER_REGEX = r'^Screen\sShot.*?\sat\s.*?\.png'


def _get_args():
    parser = ArgumentParser(version=__VERSION__)
    parser.add_argument(
        '-c',
        '--config',
        metavar='PATH',
        help='Path to a config file',
        default=DEFAULT_CONFIG_FILE)
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
        '-m',
        '--matcher',
        metavar='REGEX',
        help='RegEx string to match files against for upload',
        default=DEFAULT_MATCHER_REGEX)
    parser.add_argument(
        '-V',
        '--verbose',
        help='Increase logging verbosity',
        action='store_true',
        default=DEFAULT_DIR)

    return parser.parse_args()


def _get_config(args):
    args_dict = vars(args)
    Config = namedtuple('Config', args_dict.keys()) #pylint: disable=invalid-name
    config = Config(**args_dict)

    if path.exists(args.config):
        logging.info('Loading config from %s', args.config)
        with open(args.config) as config_file:
            parsed_config = yaml.safe_load(config_file.read())
            if parsed_config is not None:
                new_config = args_dict.copy()
                new_config.update(parsed_config)
                config = Config(**new_config)

    return config


def run():
    """
    Run the CLI tool
    """

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    args = _get_config(_get_args())
    observer = Observer()

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
