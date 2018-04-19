#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Yeolar
#

import os
import subprocess
import time

from puppytools.util.colors import *


def which(*cmds):
    for cmd in cmds:
        if subprocess.call(['which', cmd], stdout=subprocess.PIPE) == 0:
            return cmd
    return None


def run(cmd, timing=False):
    print cyan(cmd, True)
    if timing:
        t = time.time()
        os.system(cmd)
        print red('Cost: %.2fs' % (time.time() - t), True)
    else:
        os.system(cmd)

