#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Yeolar
#

import argparse
import os
import sys
import textwrap

from puppytools.util.colors import *


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]

MAP_SPLIT = ' = '
INPUT_FLAG = '{INPUT}'
INPUT_SFLAG = '{I}'
OUTPUT_FLAG = '{OUTPUT}'
OUTPUT_SFLAG = '{O}'


def parse_rename_map(map_file):
    rename_map = {}
    index = 1

    if map_file:
        for line in map_file:
            if os.pathsep in line:
                ap.error('Should not use path seperator in filename.')

            if MAP_SPLIT not in line:
                rename_map[line.strip()] = str(index)
                index += 1
                continue

            input_base, _, output_base = line.partition(MAP_SPLIT)
            input_base = input_base.strip()
            output_base = output_base.strip()
            if output_base:
                rename_map[input_base] = output_base

    return rename_map


def generate_filename(input, rename_map, args):
    if args.directory:
        dirname = os.path.abspath(args.directory)
    else:
        dirname = os.path.dirname(input)

    input_base, input_ext = os.path.splitext(os.path.basename(input))
    output_base = '%s%s%s' % (args.prefix or '',
                              rename_map.get(input_base, input_base),
                              args.suffix or '')
    if args.append_extension:
        output_base += input_ext

    return os.path.join(dirname, '%s.%s' % (output_base, args.extension))


def convert(input, output, args):
    command = args.command
    command = command.replace(INPUT_FLAG, '"%s"' % input)
    command = command.replace(INPUT_SFLAG, '"%s"' % input)
    command = command.replace(OUTPUT_FLAG, '"%s"' % output)
    command = command.replace(OUTPUT_SFLAG, '"%s"' % output)

    if args.examine or args.verbose:
        print command
        if args.examine:
            return

    if os.system(command) != 0:
        print 'ERROR: execute command error.'
        sys.exit(1)


def description():
    return '''A file converter, actually it can handle all input/output command.

converting command format:
  cmd [--options ...] -o {OUTPUT} {INPUT}

  {INPUT} and {OUTPUT} will be replaced, and can be specified as
  {I}, {O} for short.
  e.g. inkscape -z --export-dpi=72 -C --export-png={OUTPUT} {INPUT}

rename map file format:
  "INPUT_BASENAME = OUTPUT_BASENAME" as each line pattern of the file.
  Note the split chars is " = ".
  An alternative pattern is "INPUT_BASENAME" for each line, when the output's
  basename will be increasing number start from 1.'''


def main():
    ap = argparse.ArgumentParser(
            prog='pp-' + PROG_NAME,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(description()),
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('input', nargs='+',
                    help='input file')
    ap.add_argument('-C', '--conv-command', action='store', dest='command',
                    required=True, help='internal called converting command')
    ap.add_argument('-e', '--extension', action='store', dest='extension',
                    required=True, help='output file extension')
    ap.add_argument('-a', '--append-extension', action='store_true',
                    dest='append_extension',
                    help='append extension instead of replacement')
    ap.add_argument('-p', '--name-prefix', action='store', dest='prefix',
                    help='set basename prefix')
    ap.add_argument('-s', '--name-suffix', action='store', dest='suffix',
                    help='set basename suffix')
    ap.add_argument('-m', '--rename-mapfile', action='store', dest='rename_map',
                    type=file, help='rename map file')
    ap.add_argument('-d', '--directory', action='store', dest='directory',
                    help='output directory, default to the same as input')
    ap.add_argument('-x', '--examine', action='store_true', dest='examine',
                    help='examine but not really do')
    ap.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                    help='show details')
    args = ap.parse_args()

    if args.command.count(INPUT_FLAG) + args.command.count(INPUT_SFLAG) != 1:
        ap.error('INPUT flag setup error in command.')
    if args.command.count(OUTPUT_FLAG) + args.command.count(OUTPUT_SFLAG) != 1:
        ap.error('OUTPUT flag setup error in command.')

    if args.directory:
        if not os.path.exists(args.directory):
            os.makedirs(args.directory, mode=0755)
        elif not os.path.isdir(args.directory):
            ap.error('invalid output directory.')

    rename_map = parse_rename_map(args.rename_map)

    for input in args.input:
        if os.path.isfile(input):
            input = os.path.abspath(input)
            output = generate_filename(input, rename_map, args)
            convert(input, output, args)
        else:
            print 'WARNING: file not found: "%s"' % input


if __name__ == '__main__':
    main()

