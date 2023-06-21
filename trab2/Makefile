# part of the makefile
minic:	minic.l minic.y
		bison -d minic.y
		flex minic.l
		cc -o $@ minic.tab.c lex.yy.c -lfl