#!/usr/bin/env python3

import fileinput

tokens = set()

with fileinput.input() as _in:
    for line in _in:
        terms = line.split()
        [_, token, _] = terms
        if token not in tokens:
            tokens.add(token)
            print("%token {}".format(token))
