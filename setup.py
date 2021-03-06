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
            'pp-addr2line = puppytools.addr2line:main',
            'pp-bazel2cmake = puppytools.bazel2cmake:main',
            'pp-cf = puppytools.codefmt:main',
            'pp-cf2 = puppytools.codefmt:main2',
            'pp-cf4 = puppytools.codefmt:main4',
            'pp-convert = puppytools.converter:main',
            'pp-genstrings = puppytools.genstrings:main',
            'pp-htmlparser = puppytools.htmlparser:main',
            'pp-ipsender = puppytools.ipsender:main',
            'pp-rh = puppytools.rh:main',
            'pp-sed = puppytools.sed:main',
            'pp-wc = puppytools.wc:main',
        ]
    },
)
