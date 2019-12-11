# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from color import generateColorFunction


def on(msg):
    return generateColorFunction('green')(msg)


def off(msg):
    return generateColorFunction('red')(msg)


def notice(msg):
    return generateColorFunction('purple')(msg)


def hint(msg):
    return generateColorFunction('yellow')(msg)


def success(msg):
    return generateColorFunction('green')(msg)


def warn(msg):
    return generateColorFunction('yellow')(msg)


def error(msg):
    return generateColorFunction('red')(msg)


def system(msg):
    return generateColorFunction('light-red')(msg)


def exit(msg):
    return generateColorFunction('red')(msg)


def breakpoint(msg):
    return generateColorFunction('yellow')(msg)


def signal(msg):
    return generateColorFunction('bold,red')(msg)


def prompt(msg):
    return generateColorFunction('bold,red')(msg)
