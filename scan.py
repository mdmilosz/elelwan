#!/usr/bin/env python3

import fileinput

print('''\
%{
  #include <stdio.h>
  int yywrap(void);
  int yylex(void);
  #include "Lpars.h"
  extern int LLlval;
%}
%% \
''')

with fileinput.input() as _in:
    for i, line in enumerate(_in):
        terms = line.split()
        [word, token, _] = terms
        print('{}\t{{ LLlval = {}; return {}; }}'.format(word, i, '_'+token))
    
print('''\
[ \\t\\n]\t;
.\t{{ printf("Error\\n"); exit(-1); }}
%%
int yywrap(void) { return 1; } \
''')
