#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, Yeolar <yeolar@gmail.com>
#

from setuptools import setup, find_packages


setup(
    name='puppy-tools',
    version='0.1',
    description='puppy-tools is a collection of simple and easy-used tools',
    long_description=open('README.md').read().split('\n\n', 1)[1],
    author='Yeolar',
    author_email='yeolar@gmail.com',
    url='http://www.yeolar.com',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'pp-sed = puppy-tools.sed:main',
        ]
    },
)
