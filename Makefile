DICT?=dict.txt
GRAM?=gram.txt
OUT?=out

.PHONY: all
all: $(OUT)

$(OUT): lex.yy.c gram.c dict.c
	gcc -o $(OUT) lex.yy.c Lpars.c gram.c dict.c

lex.yy.c: scan.l
	flex -l scan.l

scan.l: scan.py $(DICT)
	./scan.py $(DICT) > scan.l

gram.c: gram.g
	LLgen gram.g

gram.g: gram.py $(GRAM) $(DICT)
	./tokens.py $(DICT) | ./gram.py - $(GRAM) > gram.g

dict.c: dict.py $(DICT)
	./dict.py $(DICT) > dict.c

.PHONY: test
test: $(OUT)
	./$(OUT) < test.txt

.PHONY: clean
clean:
	rm -f lex.yy.c
	rm -f scan.l
	rm -f Lpars.c
	rm -f Lpars.h
	rm -f gram.c
	rm -f gram.g
	rm -f dict.c
