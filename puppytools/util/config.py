#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

import imp
import os
import sys

from puppytools.util.colors import *


def load_config(conf_name):
    file = conf_name + '.cfg'
    path = os.path.expanduser(os.path.join('~/.puppy', file))
    conf = imp.new_module('conf')
    try:
        with open(path) as fp:
            exec fp.read() in conf.__dict__
    except IOError:
        print red('Missing conf: %s' % path, True)
        sys.exit(1)
    return conf

