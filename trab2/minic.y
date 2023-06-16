/*
 * This grammar sourced from:
 *   http://www.lysator.liu.se/c/ANSI-C-grammar-y.html
 */

%{

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

%start function

%%

function
	: type ID LBRACKET arg_list RBRACKET compound_stmt
	| type ID LBRACKET arg_list RBRACKET compound_stmt function_
	;

function_
	: function
	;

arg_list
	: arg arg_list_
	;

arg_list_
	: COMMA arg arg_list_
	;

arg
	: type ID 
	;

declaration
	: type ident_list PCOMMA
	;

type
	: INT 
	| FLOAT 
	| CHAR 
	;

ident_list
	: ID ident_list_ 
	;

ident_list_
	: COMMA ident_list
	;

stmt
	: for_stmt 
	| while_stmt 
	| expr PCOMMA 
	| if_stmt 
	| compound_stmt 
	| declaration 
	| PCOMMA 
	;

for_stmt
	: FOR LBRACKET expr PCOMMA opt_expr PCOMMA opt_expr RBRACKET stmt
	;

opt_expr
	: expr
	;

while_stmt
	: WHILE LBRACKET expr RBRACKET stmt 
	;

if_stmt
	: IF LBRACKET expr RBRACKET stmt else_part
	;

else_part
	: ELSE stmt
	;

compound_stmt
	: LBRACE stmt_list RBRACE
	;

stmt_list
	: stmt stmt_list
	| function stmt_list
	;

expr
	: ID ATTR expr
	| r_value
	;

r_value
	: mag r_value_
	;

r_value_
	: compare mag r_value_
	;

compare
	: EQ 
	| LT
	| GT
	| LE
	| GE
	| NE
	;

mag
	: term mag_
	;

mag_
	: PLUS term mag_
	| MINUS term mag_
	;

term
	: factor term_
	;

term_
	: MULT factor term_
	| DIV factor term_
	;

factor
	: LBRACKET expr RBRACKET
	| MINUS factor
	| PLUS factor
	| ID
	| NUMBER
	| CHAR
	;



%%
#include <stdio.h>

extern char yytext[];
extern int column;

yyerror(s)
char *s;
{
	fflush(stdout);
	printf("\n%*s\n%*s\n", column, "^", column, s);
}

