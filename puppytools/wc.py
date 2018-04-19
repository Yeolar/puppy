#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 Yeolar
#

import argparse
import os
import sys

from puppytools.util.colors import *


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]


def extend_directories(paths):
    all_files = []
    for path in paths:
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for name in files:
                    all_files.append(os.path.join(root, name))
        else:
            all_files.append(path)
    return all_files


def calc_file_lines(file):
    with open(file) as fp:
        return len(fp.readlines())


def main():
    ap = argparse.ArgumentParser(
            prog='pp-' + PROG_NAME,
            description='wc',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('input', nargs='+',
                    help='input file')
    ap.add_argument('-l', '--lines', action='store_true', dest='line_mode',
                    help='print the newline counts')
    ap.add_argument('-r', '--recursive', action='store_true', dest='recursive',
                    help='operate recursively')
    args = ap.parse_args()

    if args.recursive:
        input_files = extend_directories(args.input)
    else:
        input_files = [f for f in args.input if os.path.isfile(f)]

    d = {}

    if args.line_mode:
        for f in input_files:
            d[f] = calc_file_lines(f)
        n = sum(d.values())
        for f, i in sorted(d.items()):
            print '%7d' % i, f
        print '%7d' % n, 'total'
    else:
        ap.error('No counting option specified')


if __name__ == '__main__':
    main()

