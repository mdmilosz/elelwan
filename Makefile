SCANNER_DESC_FILE=scan.l
PARSER_DESC_FILE=gram.g
PARSER_EXEC_FILE=out

all: $(PARSER_EXEC_FILE)

$(PARSER_EXEC_FILE): lex.yy.c gram.c dict.c
	gcc -o $(PARSER_EXEC_FILE) lex.yy.c Lpars.c gram.c

lex.yy.c: $(SCANNER_DESC_FILE)
	flex -l $(SCANNER_DESC_FILE)

$(SCANNER_DESC_FILE): scan.py dict.txt
	./scan.py dict.txt > $(SCANNER_DESC_FILE)

gram.c: $(PARSER_DESC_FILE)
	LLgen $(PARSER_DESC_FILE)

$(PARSER_DESC_FILE): gram.py gram.txt
	./gram.py gram.txt > $(PARSER_DESC_FILE)

dict.c: dict.py dict.txt
	./dict.py dict.txt > dict.c

test: $(PARSER_EXEC_FILE)
	./$(PARSER_EXEC_FILE) < test.txt

clean:
	rm -f lex.yy.c
	rm -f Lpars.c
	rm -f Lpars.h
	rm -f gram.c
