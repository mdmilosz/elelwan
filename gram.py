#!/usr/bin/env python3

import fileinput

print('''\
{
  #include <stdio.h>
  #include <stdlib.h>
  #include <ctype.h>
  extern int yylineno;
  void parse(void);
  
  int LLlval;
  extern const char *dict[];
  #define INDENT do {{ int i; for (i=0; i<dent; i++) printf("  "); }} while (0)
}
''')

tokens = []
start = ""

specials = ['[', ']', '*', '+', '?', '|']

with fileinput.input() as _in:
    for line in _in:
        terms = line.split()
        if terms[0] == "%token":
            tokens += terms[1:]
        elif terms[0] == "%start" and len(terms)==2:
            start = terms[1]
        elif terms[0] == "%%" and len(terms)==1:
            break
        
    print('''\
%token {};
%start parse, _start;

_start : {}(0) ;
'''.format(", ".join(['_'+t for t in tokens]), start))
        
    for line in _in:
        terms = line.split()
        if terms[1] == "=":
            parent = terms[0]
            children = terms[2:]
            print('''\
{0} (int dent) {{
    INDENT; printf("[{0}\\n");
  }} : [ \
'''.format(parent))
            for child in children:
                if child in specials:
                    print('    {}'.format(child))
                else:
                    print('    {} (dent+1)'.format(child))
            print('''\
  ] {
    INDENT; printf("]\\n");
  } ;
''')

for t in tokens:
    print('''\
{0} (int dent) {{
    INDENT; printf("[{0} ");
  }} : _{0}
  {{
    printf("%s]\\n", dict[LLlval]);
  }} ;
'''.format(t))

print('''\
{
  int main()
  {

    parse();
    return 0;
  }

  void LLmessage(int tk)
  {
    printf("LLmessage: ");
    switch(tk)
    {
      case -1 : if(isprint(LLsymb))printf("expected EOF not encountered, unexpected token (%c) found, skipping extra input\\n", LLsymb);
                else printf("expected EOF not encountered, unexpected token (%d) found, skipping extra input\\n", LLsymb);
                break;
      case 0  : if(isprint(LLsymb))printf("unexpected token (%c) deleted\\n",LLsymb);
                else printf("unexpected token (%d) deleted\\n",LLsymb);
                exit(-1);
      default : if(isprint(tk))printf("expected token (%c) not found, ", tk);
                else printf("expected token (%d) not found, ", tk);
                if(isprint(LLsymb))printf("token (%c) encountered\\n", LLsymb);
                else printf("token (%d) encountered\\n", LLsymb);
                exit(-1);
    }
  }
}
''')
