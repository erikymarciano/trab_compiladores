D			[0-9]
L			[a-zA-Z_]


%{

/* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */

void count();
#include <stdio.h>
#include "minic.tab.h"


%}


%%
"int"			{ count(); return INT; }
"float"			{ count(); return FLOAT; }
"char"			{ count(); return CHAR; }
"if"			{ count(); return IF; }
"else"			{ count(); return ELSE; }
"while"			{ count(); return WHILE; }
"for"			{ count(); return FOR; }

{L}({L}|{D})*	{ count(); return ID; }

{D}+("."{D})*	{ count(); yylval = atoi(yytext); return NUMBER; }

"<="			{ count(); return LE; }
">="			{ count(); return GE; }
"=="			{ count(); return EQ; }
"!="			{ count(); return NE; }
";"			{ count(); return PCOMMA; }
"{"		{ count(); return LBRACE; }
"}"		{ count(); return RBRACE; }
","			{ count(); return COMMA; }
"="			{ count(); return ATTR; }
"("			{ count(); return LBRACKET; }
")"			{ count(); return RBRACKET; }
"-"			{ count(); return MINUS; }
"+"			{ count(); return PLUS; }
"*"			{ count(); return MULT; }
"/"			{ count(); return DIV; }
"<"			{ count(); return LT; }
">"			{ count(); return GT; }

[ \t\v\n\f]		{ count(); }
.			{ /* ignore bad characters */ }

%%

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
