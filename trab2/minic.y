/*
 * This grammar sourced from:
 *   http://www.lysator.liu.se/c/ANSI-C-grammar-y.html
 */

%{
#include<stdio.h>
%}

%token INT FLOAT CHAR
%token IF ELSE WHILE FOR
%token PLUS MINUS MULT DIV
%token LT LE GT GE EQ NE
%token ATTR
%token COMMA PCOMMA
%token LBRACKET RBRACKET LBRACE RBRACE
%token NUMBER
%token ID

%%

function:
	| type ID LBRACKET arg_list RBRACKET compound_stmt function 
	;

arg_list: arg
	| arg_list COMMA arg
	;

arg: type ID 
	;

declaration: type ident_list PCOMMA
	;

type: INT 
	| FLOAT 
	| CHAR 
	;

ident_list: ID COMMA ident_list
	| ID
	;

stmt: for_stmt 
	| while_stmt 
	| expr PCOMMA 
	| if_stmt 
	| compound_stmt 
	| declaration 
	| PCOMMA 
	;

for_stmt: FOR LBRACKET expr PCOMMA opt_expr PCOMMA opt_expr RBRACKET stmt
	;

opt_expr: expr
	|
	;

while_stmt: WHILE LBRACKET expr RBRACKET stmt 
	;

if_stmt: IF LBRACKET expr RBRACKET stmt else_part
	;

else_part: ELSE stmt
	|
	;

compound_stmt: LBRACE stmt_list RBRACE
	;

stmt_list: stmt_list stmt
	|
	;

expr: ID ATTR expr
	| r_value
	;

r_value: r_value compare mag
	| mag
	;

compare: EQ 
	| LT
	| GT
	| LE
	| GE
	| NE
	;

mag
	: mag PLUS term
	| mag MINUS term
	| term
	;

term: term MULT factor
	| term DIV factor
	| factor
	;

factor: LBRACKET expr RBRACKET
	| MINUS factor
	| PLUS factor
	| ID
	| NUMBER
	| CHAR
	;

%%

int yyerror(char *s)
{
  fprintf(stderr, "error: %s\n", s);
}

void main(int argc, char **argv)
{
  yyparse();
}

