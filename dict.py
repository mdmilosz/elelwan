#!/usr/bin/env python3

import fileinput

print('''\
const char *dict[] = { \
''')

with fileinput.input() as _in:
    for line in _in:
        terms = line.split()
        [word, token, _eng] = terms
        eng = '  # '+_eng if _eng != '-' else ''
        print('\t"{}{}",'.format(word, eng))
    
print('''\
}; \
''')
