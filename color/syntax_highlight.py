# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
import os.path
import re

from color import message

import pygments
import pygments.lexers
import pygments.formatters
from .lexer import PwntoolsLexer

style = "monokai" 

formatter = pygments.formatters.Terminal256Formatter(style=str(style))
pwntools_lexer = PwntoolsLexer()
lexer_cache = {}

def check_style():
    global formatter
    try:
        formatter = pygments.formatters.Terminal256Formatter(
            style=str(style)
        )

    except pygments.util.ClassNotFound:
        print(message.warn("The pygment formatter style '%s' is not found, restore to default" % style))


def syntax_highlight(code, filename='.asm'):
    # No syntax highlight if pygment is not installed

    filename = os.path.basename(filename)

    lexer = lexer_cache.get(filename, None)

    # If source code is asm, use our customized lexer.
    # Note: We can not register our Lexer to pygments and use their APIs,
    # since the pygment only search the lexers installed via setuptools.
    if not lexer:
        for glob_pat in PwntoolsLexer.filenames:
            pat = '^' + glob_pat.replace('.', r'\.').replace('*', r'.*') + '$'
            if re.match(pat, filename):
                lexer = pwntools_lexer
                break

    if not lexer:
        try:
            lexer = pygments.lexers.guess_lexer_for_filename(filename, code, stripnl=False)
        except pygments.util.ClassNotFound:
            # no lexer for this file or invalid style
            pass

    if lexer:
        lexer_cache[filename] = lexer

        code = pygments.highlight(code, lexer, formatter).rstrip()

    return code
