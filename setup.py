#!/usr/bin/env python
from distutils.core import setup

url = 'https://github.com/FEE1DE4D/PyMarkovTextGenerator'
setup(
    name='PyMarkovTextGenerator',
    version='1.0.2',
    py_modules=['PyMarkovTextGenerator'],

    author='FEE1DE4D',
    author_email='fee1de4d@gmail.com',

    url=url,
    description='Random text generator base on Markov chains.',
    license='GPLv2+',

    long_description="Documentation can be found here " + url,

    classifiers=[
        "License :: OSI Approved :: GNU General Public License v2 or later ("
        "GPLv2+)",

        "Programming Language :: Python :: 2.7",

        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General"
    ],
)
