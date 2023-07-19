/*
 * This grammar sourced from:
 *   http://www.lysator.liu.se/c/ANSI-C-grammar-y.html
 */

%{
    #include<stdio.h>
    
    int cur_func_scope, cur_func_scope_level;
    extern int func_declaration;
    extern int id_declaration;
    extern int scope_counter;
    extern int scope_father;
    extern int cur_funcID;
    extern int getScopeLevel(int id);
    extern int getScopeFatherId(int id);
    extern int getTypeAtScope(char *name, int scope_id);
    extern void checkSameTypeAtArithmetic(int type1, int type2, char *op);
    extern void checkSameTypeAtComparison(int type1, int type2, char *op);
%}

%union
{
    int line;
    int type;
    char *code;
}

%token INT FLOAT CHAR
%token IF ELSE WHILE FOR
%token PLUS MINUS MULT DIV
%token LT LE GT GE EQ NE
%token ATTR
%token COMMA PCOMMA
%token LBRACKET RBRACKET LBRACE RBRACE
%token NUMBER CHARACTER
%token ID

%%

function:
	| { func_declaration = 1; cur_func_scope = scope_father; cur_func_scope_level = scope_counter; } type ID { func_declaration = 0; } LBRACKET { id_declaration = 1; scope_father = cur_funcID; cur_func_scope_level = scope_counter++; } arg_list { id_declaration = 0; } RBRACKET compound_stmt { scope_father = cur_func_scope; scope_counter = cur_func_scope_level; } function 
	;

arg_list: arg
	| arg_list COMMA arg
	;

arg: type ID 
	;

declaration: { id_declaration = 1; } type ident_list { id_declaration = 0; } PCOMMA
	;

type: INT
	| FLOAT
	| CHAR
	;

ident_list: ID COMMA ident_list
	| ID
	;

stmt: { cur_func_scope = scope_father; cur_func_scope_level = scope_counter; } for_stmt 
	| { cur_func_scope = scope_father; cur_func_scope_level = scope_counter; } while_stmt 
	| expr PCOMMA 
	| { cur_func_scope = scope_father; cur_func_scope_level = scope_counter; } if_stmt 
	| { scope_father = cur_funcID; cur_func_scope_level = scope_counter++; } compound_stmt { scope_father = getScopeFatherId(cur_func_scope); scope_counter = getScopeLevel(cur_func_scope_level); } 
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

else_part: { cur_func_scope = scope_father; cur_func_scope_level = scope_counter; } ELSE stmt
	|
	;

compound_stmt: LBRACE stmt_list RBRACE
	;

stmt_list: stmt_list stmt
	|
	;

expr: ID ATTR expr { checkSameTypeAtComparison($<type>1, $<type>3, $<code>2); $<type>$ = $<type>1; }
	| r_value { $<type>$ = $<type>1; }
	;

r_value: r_value compare mag  { checkSameTypeAtComparison($<type>1, $<type>3, $<code>2); $<type>$ = $<type>1; }
	| mag  { $<type>$ = $<type>1; }
	;

compare: EQ 
	| LT 
	| GT 
	| LE 
	| GE
	| NE
	;

mag
	: mag PLUS term { checkSameTypeAtArithmetic($<type>1, $<type>3, $<code>2); $<type>$ = NUMBER; }
	| mag MINUS term { checkSameTypeAtArithmetic($<type>1, $<type>3, $<code>2); $<type>$ = NUMBER; }
	| term { $<type>$ = $<type>1; }
	;

term: term MULT factor { checkSameTypeAtArithmetic($<type>1, $<type>3, $<code>2); $<type>$ = NUMBER; }
	| term DIV factor { checkSameTypeAtArithmetic($<type>1, $<type>3, $<code>2); $<type>$ = NUMBER; }
	| factor { $<type>$ = $<type>1; }
	;

factor: LBRACKET expr RBRACKET { $<type>$ = $<type>2; }
	| MINUS factor { $<type>$ = $<type>2; }
	| PLUS factor { $<type>$ = $<type>2; }
	| ID { $<type>$ = getTypeAtScope($<code>1, cur_funcID); }
	| NUMBER { $<type>$ = NUMBER; }
    | CHARACTER { $<type>$ = CHARACTER; }
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
