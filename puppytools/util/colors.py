#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Yeolar
#

import sys

try:
    import curses
except ImportError:
    curses = None


def _stderr_supports_color():
    color = False
    if curses and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
        try:
            curses.setupterm()
            if curses.tigetnum("colors") > 0:
                color = True
        except Exception:
            pass
    return color


class ColorFormatter(object):

    def __init__(self):
        if _stderr_supports_color():
            fg_color = (curses.tigetstr('setaf') or
                        curses.tigetstr('setf') or '')
            self._colors = dict(enumerate(
                [curses.tparm(fg_color, i) for i in range(8)]))
            self._bold = curses.tigetstr('bold')
            self._normal = curses.tigetstr('sgr0')
        else:
            self._colors = {}
            self._bold = ''
            self._normal = ''

    def format(self, text, color_no, bold=False):
        return (self._colors.get(color_no, self._normal)
                + (self._bold if bold else '')
                + str(text) + self._normal)


_formatter = ColorFormatter()

def _wrap_with(code):

    def inner(text, bold=False):
        return _formatter.format(text, code, bold)
    return inner

red = _wrap_with(1)
green = _wrap_with(2)
yellow = _wrap_with(3)
blue = _wrap_with(4)
magenta = _wrap_with(5)
cyan = _wrap_with(6)
white = _wrap_with(7)

