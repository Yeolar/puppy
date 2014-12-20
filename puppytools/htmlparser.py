#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, Yeolar <yeolar@gmail.com>
#

import argparse
import urllib2
from HTMLParser import HTMLParser


PROG_NAME = 'pp-htmlparser'


class SingleParser(HTMLParser):

    def __init__(self, tag, attr, parse_data, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        self._tag = tag
        self._attr = attr
        self._parse_data = parse_data
        self._match = False             # for print data
        self._start = None              # for print all

    def handle_starttag(self, tag, attrs):
        if tag == self._tag:
            if self._attr:
                for attr in attrs:
                    if attr[0] == self._attr:
                        if self._parse_data:
                            self._match = True
                        else:
                            print attr[1]
            else:
                if self._parse_data:
                    self._match = True
                else:
                    self._start = self.getpos()

    def handle_endtag(self, tag):
        if tag == self._tag:
            if self._parse_data:
                self._match = False
            if not self._attr and not self._parse_data:
                if self._start:
                    end = self.getpos()
                    self.print_rawdata(self._start, end)
                    self._start = None

    def handle_data(self, data):
        if self._match:
            print data

    def print_rawdata(self, start, end):    # untest
        lines = self.rawdata.splitlines(True)
        if start[0] == end[0]:
            print lines[start[0]][start[1]:end[1]]
        else:
            print lines[start[0]][start[1]:]
            for i in range(start[0] + 1, end[0]):
                print lines[i]
            print lines[end[0]][:end[1]]


def main():
    ap = argparse.ArgumentParser(
            prog=PROG_NAME,
            description='Parse html, '
                        'extract attribute value and data of html tag.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('input', nargs='+',
                    help='input file')
    ap.add_argument('-t', '--tag', action='store', dest='tag', required=True,
                    help='tag to parse')
    ap.add_argument('-a', '--attr', action='store', dest='attr',
                    help='attribute to parse')
    ap.add_argument('-d', '--data', action='store_true', dest='parse_data',
                    help='parse data')
    args = ap.parse_args()

    input_files = args.input
    if not args.attr and not args.parse_data:
        ap.error('Should specify --attr or open --data.')

    parser = SingleParser(args.tag, args.attr, args.parse_data)

    for input_file in input_files:
        if input_file.startswith('http://'):
            fp = urllib2.urlopen(input_file)
            parser.feed(fp.read())
            parser.reset()
            fp.close()
        else:
            with open(input_file) as fp:
                parser.feed(fp.read())
                parser.reset()

    parser.close()


if __name__ == '__main__':
    main()

