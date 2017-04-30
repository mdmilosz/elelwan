DICT?=dict.txt
GRAM?=gram.txt
OUT?=out

all: $(OUT)

$(OUT): lex.yy.c gram.c dict.c
	gcc -o $(OUT) lex.yy.c Lpars.c gram.c

lex.yy.c: scan.l
	flex -l scan.l

scan.l: scan.py $(DICT)
	./scan.py $(DICT) > scan.l

gram.c: gram.g
	LLgen gram.g

gram.g: gram.py $(GRAM)
	./gram.py $(GRAM) > gram.g

dict.c: dict.py $(DICT)
	./dict.py $(DICT) > dict.c

test: $(OUT)
	./$(OUT) < test.txt

clean:
	rm -f lex.yy.c
	rm -f scan.l
	rm -f Lpars.c
	rm -f Lpars.h
	rm -f gram.c
	rm -f gram.g
	rm -f dict.c
