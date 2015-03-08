#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Yeolar <yeolar@gmail.com>
#

import argparse
import os
import re


PROG_NAME = 'pp-genstrings'


STR_RE = '\s*@"[^"]+"\s*'
VAR_RE = '\s*\w+\s*'

BASE_RE    = ('%%s\s*\((%(s)s),(%(s)s|%(v)s)\)'
                % {'s': STR_RE, 'v': VAR_RE})
TABLE_RE   = ('%%sFromTable\s*\((%(s)s),(%(s)s),(%(s)s|%(v)s)\)'
                % {'s': STR_RE, 'v': VAR_RE})
BUNDLE_RE  = ('%%sFromTableInBundle\s*\((%(s)s),(%(s)s),%(v)s,(%(s)s|%(v)s)\)'
                % {'s': STR_RE, 'v': VAR_RE})
DEFAULT_RE = ('%%sWithDefaultValue\s*\((%(s)s),(%(s)s),%(v)s,%(s)s,(%(s)s|%(v)s)\)'
                % {'s': STR_RE, 'v': VAR_RE})


def prepare_patterns(routine):
    base_patterns = []
    table_patterns = []

    if not routine:
        routine = ('NSLocalizedString', 'CFCopyLocalizedString')
    else:
        routine = (routine,)

    for r in routine:
        base_patterns.append(BASE_RE % r)
        table_patterns.append(TABLE_RE % r)
        table_patterns.append(BUNDLE_RE % r)
        table_patterns.append(DEFAULT_RE % r)

    return base_patterns, table_patterns


def create_table(table_dict, table_key, directory, append):
    if table_key not in table_dict:
        table_dict[table_key] = {}

    if not append:
        return

    with open(os.path.join(directory, table_key + '.strings')) as fp:
        table = '\n'.join([l.strip() for l in fp.readlines()])
        for block in table.split('\n\n'):
            comment_block, _, kv_block = block.partition('*/')
            comments = comment_block[2:].strip().split('\n')
            m = re.match('^"([^"]+)" = "([^"]+)";', kv_block)
            if m:
                table_dict[table_key][m.group(1)] = (m.group(2), [], comments)


def update_table(table_dict, table_key, key, comment):
    table_key = table_key.strip().strip('@"')
    key = key.strip().strip('@"')
    comment = comment.strip().strip('@"')

    old_value = table_dict[table_key][key][0]
    old_comments = table_dict[table_key][key][2]

    if key not in table_dict[table_key]:
        table_dict[table_key][key] = (key, [comment])
    else:
        if comment not in old_comments:
            table_dict[table_key][key] = (key, [comment], old_comments)
        else:
            table_dict[table_key][key][1].append(comment)


def extract(f, table_dict, base_patterns, table_patterns, args):
    output_dir = args.output_dir

    with open(f) as fp:
        src = ''.join([l.strip() for l in fp.readlines()])
        for p in base_patterns:
            for m in p.finditer(src):
                create_table(table_dict, 'Localized', output_dir, args.append)
                update_table(table_dict, 'Localized', m.group(1), m.group(2))
        for p in table_patterns:
            for m in p.finditer(src):
                if args.table == m.group(2):  # skip table
                    continue
                create_table(table_dict, m.group(2), output_dir, args.append)
                update_table(table_dict, m.group(2), m.group(1), m.group(3))


def sync(table_dict, output_dir, args):
    def sort_key(l):
        return sorted(l, cmp=lambda x,y: cmp(x.lower(), y.lower()))[0].lower()

    for table_key in table_dict:
        with open(os.path.join(output_dir, table_key + '.strings'), 'w') as fp:
            if args.comment_sorted:
                table = sorted(table_dict[table_key].items(),
                        cmp=lambda x,y: cmp(sort_key(x[1]), sort_key(y[1])))
            else:
                table = sorted(table_dict[table_key].items(),
                        cmp=lambda x,y: cmp(x[0].lower(), y[0].lower()))

            for key, value in table:
                if len(value[1]) > 1 and not args.quiet:
                    print 'Warning: Key "%s" used with multiple comments %s' % (
                            key, ' & '.join(['"%s"' for c in value[1]]))
                fp.write('/* ' + value[1][0])
                for comment in value[1][1:]:
                    fp.write('\n   ' + comment)
                fp.write(' */\n')
                fp.write('"%s" = "%s";\n\n' % (key, value[0]))


def description():
    return ("A similar tool of Mac's genstrings. "
            "Enhance the appending and entry sorted.")


def main():
    ap = argparse.ArgumentParser(
            prog=PROG_NAME,
            description=description(),
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('input', nargs='+',
                    help='input file')
    ap.add_argument('-a', action='store_true', dest='append',
                    help='append mode')
    ap.add_argument('-s', action='store', dest='routine',
                    help='substitute routine for NSLocalizedString')
    ap.add_argument('--skip_table', action='store', dest='table',
                    help='skip over the file for table')
#    ap.add_argument('--no_positional_param', action='store_true',
#                    dest='no_positional_param',
#                    help='turn off generation of positional parameters')
    ap.add_argument('--comment_sorted', action='store_true',
                    dest='comment_sorted',
                    help='sorted by comment, default by key')
    ap.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                    help='turn off multiple key/value pairs warning')
    ap.add_argument('-o', '--output_dir', action='store', dest='output_dir',
                    help='output directory')
    args = ap.parse_args()

    input_files = args.input

    base_patterns, table_patterns = prepare_patterns(args.routine)
    table_dict = {}

    for input in input_files:
        if os.path.isfile(input):
            extract(input, table_dict, base_patterns, table_patterns, args)
        else:
            print "Ignore non-regular file path: '%s'" % input

    sync(table_dict, args.output_dir, args)


if __name__ == '__main__':
    main()

