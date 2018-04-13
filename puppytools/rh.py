#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

import argparse
import os

from puppytools.util.cmd import run
from puppytools.util.colors import *
from puppytools.util.config import load_config


PROG_NAME = os.path.splitext(os.path.basename(__file__))[0]

CONF = load_config(PROG_NAME)


def list():
    for i, (name, ip, group) in enumerate(CONF.HOSTS):
        print white('%2d: %22s %-14s %s' % (i, name, ip, group), True)


def connect(host):
    try:
        i = int(host)
        host = CONF.HOSTS[i][1]
    except:
        pass
    run('ssh %s@%s' % (CONF.USER, host))


def main():
    ap = argparse.ArgumentParser(
            prog='pp-' + PROG_NAME,
            description='Remote Host.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('-l', '--list', action='store_true',
                    dest='list',
                    help='list all remote hosts')
    ap.add_argument('-c', '--connect', action='store',
                    dest='host', metavar='RH',
                    help='connect to remote host')
    args = ap.parse_args()

    if args.list:
        list()
        return
    if args.host:
        connect(args.host)
        return

    ap.print_help()


if __name__ == '__main__':
    main()

