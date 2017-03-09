"""
Setup module
"""

# pylint: disable=C0103,redefined-builtin
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_desc = f.read()

setup(
    name='screenbase',
    version='1.0.0',
    description='Tool for automatically copying screenshots into your Keybase public folder',
    long_description=long_desc,
    url='https://github.com/jlindsey/screenbase',
    author='Josh Lindsey',
    author_email='joshua.s.lindsey@gmail.com',
    packages=find_packages(exclude=['docs', 'tests']),
    license='GPL-3.0+',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
    ],
    keywords='screenshots keybase',
    install_requires=[
        'watchdog>=0.8.2',
        'pyperclip>=1.5.27'
    ],
    entry_points={
        'console_scripts': [
            'screenbase=screenbase.cli:run'
        ]
    }
)
