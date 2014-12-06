#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2014, Yeolar <yeolar@gmail.com>
#

import argparse
import ConfigParser
import os


PROG_NAME = 'pp-config'

DEFAULT_CONF_FILE = '~/.puppytools/puppytools.cfg'

DEFAULT_CONF = {
    'pp-ipsender': dict(
        ifname='ppp0',
        record_file='~/.puppytools/ipsender/%(ifname)s-ip.txt',
        mail_server='smtp.qq.com',
        mail_user='',
        mail_pass='',
        mail_from='',
        mail_to='',
        mail_subject='System Notice',
    ),
}

class Config(dict):

    def __init__(self, conf_file=DEFAULT_CONF_FILE):
        self._conf = ConfigParser.ConfigParser()
        self._conf_file = os.path.expanduser(conf_file)

        if os.path.exists(self._conf_file):
            return

        for k, v in DEFAULT_CONF.items():
            self._set_section(k, v)

        os.makedirs(os.path.dirname(self._conf_file))

        with open(os.path.expanduser(self._conf_file), 'wb') as fp:
            self._conf.write(fp)

    def _set_section(self, section, conf_value):
        self._conf.add_section(section)
        for k, v in conf_value.items():
            self._conf.set(section, k, v)

    def _get_section(self, section):
        for k in DEFAULT_CONF[section].keys():
            self.__setattr__(k, self._conf.get(section, k))

    def read_config(self, section, conf_file=None):
        f = os.path.expanduser(conf_file) if conf_file else self._conf_file
        with open(f) as fp:
            self.read_config_fp(fp)

    def read_config_fp(self, section, conf_fp):
        self._conf.readfp(conf_fp)
        self._get_section(section)


def main():
    ap = argparse.ArgumentParser(
            prog=PROG_NAME,
            description='Config puppy-tools.',
            epilog='Author: Yeolar <yeolar@gmail.com>')
    ap.add_argument('-v', '--version', action='version',
                    version='%(prog)s - by Yeolar <yeolar@gmail.com>')
    args = ap.parse_args()

    Config(DEFAULT_CONF_FILE)


if __name__ == '__main__':
    main()

