#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

import argparse
import os
import re

from puppytools.util.colors import *


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]

PATTERN = re.compile('(.*)\(\) \[(.*)\]')


def collect_multi_lines():
    lines = []
    line = raw_input()
    while line:
        lines.append(line)
        line = raw_input()
    return lines


def print_trace(text):
    m = PATTERN.match(text)
    if m:
        binary, pos = m.groups()
        os.system('addr2line -e %s %s' % (binary, pos))
    else:
        print yellow('ignore: %s' % text)


def main():
    lines = collect_multi_lines()
    for line in lines:
        print_trace(line)


if __name__ == '__main__':
    main()

