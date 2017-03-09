"""
Container module for watchdog subclasses
"""
# pylint: disable=invalid-name

from __future__ import absolute_import, print_function, unicode_literals

import hashlib
import logging
import os
import re
import shutil
import subprocess
from distutils.spawn import find_executable

from watchdog.events import FileCreatedEvent, FileSystemEventHandler

import pyperclip


def _notify(url):
    if not find_executable('terminal-notifier'):
        logging.debug('termina-notifier not found on PATH')
        return

    cmd = [
        'terminal-notifier',
        '-message', 'Uploaded to keybase.io',
        '-title', 'Screenbase',
        '-subtitle', 'Click to open',
        '-group', 'screenbase',
        '-open', url,
        '-timeout', '4'
    ]

    subprocess.check_output(cmd)


class ScreenshotWatcher(FileSystemEventHandler):
    """
    Primary screenshot watcher class
    """

    def __init__(self, args):
        self.args = args
        self.keybase_dir = os.path.join(os.sep, 'keybase', 'public', args.user,
                                        'screenbase')

        if not os.path.exists(self.keybase_dir):
            logging.info('Creating screenshots directory at %s',
                         self.keybase_dir)
            os.mkdir(self.keybase_dir)

    def on_created(self, event):
        self._handle_event(event)

    def on_moved(self, event):
        self._handle_event(event)

    def _handle_event(self, event):
        moved = None
        filepath = event.src_path if isinstance(
            event, FileCreatedEvent) else event.dest_path

        if re.match(r'^Screen\sShot.*?\sat\s.*?\.png',
                    os.path.basename(filepath)):
            moved = self._move_screenshot(filepath)
        else:
            logging.debug('Ignoring event: path does not match regex')
            return

        url = self._copy_to_clipboard(moved)
        _notify(url)

    def _move_screenshot(self, filepath):
        hasher = hashlib.md5()
        _, ext = os.path.splitext(filepath)
        with open(filepath, 'r') as f:
            hasher.update(f.read())
        dest_name = hasher.hexdigest() + ext
        dest_path = os.path.join(self.keybase_dir, dest_name)

        logging.debug('Moved %s => %s', filepath, dest_path)
        shutil.move(filepath, dest_path)
        return dest_path

    def _copy_to_clipboard(self, filepath):
        url = 'https://%s.keybase.pub/screenbase/%s' % (
            self.args.user, os.path.basename(filepath))
        logging.info('Uploaded to %s', url)
        pyperclip.copy(url)
        logging.debug('Copied to clipboard')

        return url
