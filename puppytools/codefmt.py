#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017, Yeolar
#

import argparse
import subprocess
import os
import sys

from puppytools.util.cmd import which


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]

CF_CMD = which('clang-format', 'clang-format-3.5')


def format_cpp(input, indent=0):
    output = subprocess.check_output(CF_CMD, stdin=input)
    output = '\n'.join([
        (' '*indent + line if line else '') for line in output.splitlines()
    ])
    print output,


def main(indent=0):
    ap = argparse.ArgumentParser(
            prog='pp' + PROG_NAME,
            description='Code formatter.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('input', nargs='?', type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='input')
    ap.add_argument('-i', '--indent', type=int,
                    default=0,
                    help='global indent, default=0')
    args = ap.parse_args()

    format_cpp(args.input, indent=indent or args.indent)


def main2(): main(2)
def main4(): main(4)


if __name__ == '__main__':
    main()

