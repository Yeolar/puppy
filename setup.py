#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, Yeolar <yeolar@gmail.com>
#

from setuptools import setup, find_packages


setup(
    name='puppytools',
    version='0.1',
    description='puppy-tools is a collection of simple and easy-used tools',
    long_description=open('README.md').read(),
    license='GPLv2',
    author='Yeolar',
    author_email='yeolar@gmail.com',
    url='http://www.yeolar.com',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'pp-config = puppytools.config:main',
            'pp-convert = puppytools.converter:main',
            'pp-htmlparser = puppytools.htmlparser:main',
            'pp-ipsender = puppytools.ipsender:main',
            'pp-sed = puppytools.sed:main',
        ]
    },
)
