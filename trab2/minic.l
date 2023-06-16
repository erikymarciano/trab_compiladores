D			[0-9]
L			[a-zA-Z_]
H			[a-fA-F0-9]
E			[Ee][+-]?{D}+
FS			(f|F|l|L)
IS			(u|U|l|L)*


%{

/* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */

void count();
int yylineno = 0;
#include <stdio.h>
#include <string.h>
#include "Python.h"
#define YYSTYPE void *
#include "tokens.h"
extern void *py_parser;
extern void (*py_input)(PyObject *parser, char *buf, int *result, int max_size);
#define returntoken(tok) /*printf("%d=%s\n", tok, yytext);*/ yylval = PyString_FromString(strdup(yytext)); return (tok);
#define YY_INPUT(buf,result,max_size) { (*py_input)(py_parser, buf, &result, max_size); }

%}


%%
"int"			{ count(); returntoken(INT); }
"float"			{ count(); returntoken(FLOAT); }
"char"			{ count(); returntoken(CHAR); }
"if"			{ count(); returntoken(IF); }
"else"			{ count(); returntoken(ELSE); }
"while"			{ count(); returntoken(WHILE); }
"for"			{ count(); returntoken(FOR); }

"{D}*"			{ count(); returntoken(NUMBER); }
"for"			{ count(); returntoken(ID); }

{L}({L}|{D})*	{ count(); returntoken(check_type()); }

{D}+("."{D})*	{ count(); returntoken(NUMBER); }

"<="			{ count(); returntoken(LE); }
">="			{ count(); returntoken(GE); }
"=="			{ count(); returntoken(EQ); }
"!="			{ count(); returntoken(NE); }
";"			{ count(); returntoken(PCOMMA); }
("{"|"<%")		{ count(); returntoken(LBRACE); }
("}"|"%>")		{ count(); returntoken(RBRACE); }
","			{ count(); returntoken(COMMA); }
"="			{ count(); returntoken(ATTR); }
"("			{ count(); returntoken(LBRACKET); }
")"			{ count(); returntoken(RBRACKET); }
"-"			{ count(); returntoken(MINUS); }
"+"			{ count(); returntoken(PLUS); }
"*"			{ count(); returntoken(MULT); }
"/"			{ count(); returntoken(DIV); }
"<"			{ count(); returntoken(LT); }
">"			{ count(); returntoken(GT); }

[ \t\v\n\f]		{ count(); }
.			{ /* ignore bad characters */ }

%%

yywrap()
{
	return(1);
}


int column = 0;

void count()
{
	int i;

	for (i = 0; yytext[i] != '\0'; i++)
		if (yytext[i] == '\n')
			column = 0;
		else if (yytext[i] == '\t')
			column += 8 - (column % 8);
		else
			column++;

	/*ECHO*/;
}



int check_type()
{
/*
* pseudo code --- this is what it should check
*
*	if (yytext == type_name)
*		return(TYPE_NAME);
*
*	return(IDENTIFIER);
*/

/*
*	it actually will only return IDENTIFIER
*/

	return(IDENTIFIER);
}
