Screenbase
==========

A very simple tool that monitors your desktop for new screenshots, moves them to
your `public Keybase filesystem <https://keybase.io/docs/kbfs>`_, and copies the
link to your clipboard.

Works on macOS and (probably) Linux.

Dependencies
------------

On macOS, install `terminal-notifier` from homebrew to have notifications when
complete.

Installation
------------

Simply:

.. code-block:: bash

  $ pip install screenbase


Usage
-----

By default, screenbase watches your ``~/Desktop`` directory for files matching a regex
tailored to macOS screenshot filenames (``Screen Shot 2017-03-09 at 5.29.50 PM.png``).
This regex is configurable as a string passed with the ``-m`` flag. The watch
directory is configurable via the ``-d`` flag.

Similarly, screenbase uses your current username (via Python's ``getpass.getuser()``)
as your keybase username by default, which it uses to move files into your kbfs public
folder and generate the URL to it. This can be configured via the ``-u`` flag.

Screenbase will look for a YAML-formatted config file in
``~/.config/screenbase`` (this path configurable with the ``-c`` flag). If it
finds it, it will overload the default configs with the values it contains. The
keys should match the long form of the command line flags you can see via
``--help``. Eg:

.. code-block:: yaml

   ---
   user: jlindsey
   directory: /Users/jlindsey/screenshots
   verbose: True


License
-------

Copyright (C) 2017 Joshua Lindsey <joshua.s.lindsey@gmail.com>

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, see <http://www.gnu.org/licenses>.
