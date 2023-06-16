#!/usr/bin/env python

"""
PyBison file automatically generated from grammar file minic.y
You can edit this module, or import it and subclass the Parser class
"""

import sys

from bison import BisonParser, BisonNode, BisonSyntaxError

bisonFile = 'minic.y'  # original bison file
lexFile = 'minic.l'    # original flex file


class Parser(BisonParser):
    """
    bison Parser class generated automatically by bison2py from the
    grammar file "minic.y" and lex file "minic.l"

    You may (and probably should) edit the methods in this class.
    You can freely edit the rules (in the method docstrings), the
    tokens list, the start symbol, and the precedences.

    Each time this class is instantiated, a hashing technique in the
    base class detects if you have altered any of the rules. If any
    changes are detected, a new dynamic lib for the parser engine
    will be generated automatically.
    """

    # -------------------------------------------------
    # Default class to use for creating new parse nodes
    # -------------------------------------------------
    defaultNodeClass = BisonNode

    # --------------------------------------------
    # basename of binary parser engine dynamic lib
    # --------------------------------------------
    bisonEngineLibName = 'minic-engine'

    # ----------------------------------------------------------------
    # lexer tokens - these must match those in your lex script (below)
    # ----------------------------------------------------------------
    tokens = ['INT', 'FLOAT', 'CHAR', 'IF', 'ELSE', 'WHILE', 'FOR', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'ATTR', 'COMMA', 'PCOMMA', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'NUMBER', 'ID']

    # ------------------------------
    # precedences
    # ------------------------------
    precedences = (
        )

    # ---------------------------------------------------------------
    # Declare the start target here (by name)
    # ---------------------------------------------------------------
    start = 'function'

    # ---------------------------------------------------------------
    # These methods are the python handlers for the bison targets.
    # (which get called by the bison code each time the corresponding
    # parse target is unambiguously reached)
    #
    # WARNING - don't touch the method docstrings unless you know what
    # you are doing - they are in bison rule syntax, and are passed
    # verbatim to bison to build the parser engine library.
    # ---------------------------------------------------------------

    def on_function(self, target, option, names, values):
        """
        function
            : type ID LBRACKET arg_list RBRACKET compound_stmt
            | type ID LBRACKET arg_list RBRACKET compound_stmt function_
        """
        return self.defaultNodeClass(
            target='function',
            option=option,
            names=names,
            values=values)

    def on_function_(self, target, option, names, values):
        """
        function_
            : function
        """
        return self.defaultNodeClass(
            target='function_',
            option=option,
            names=names,
            values=values)

    def on_arg_list(self, target, option, names, values):
        """
        arg_list
            : arg arg_list_
        """
        return self.defaultNodeClass(
            target='arg_list',
            option=option,
            names=names,
            values=values)

    def on_arg_list_(self, target, option, names, values):
        """
        arg_list_
            : COMMA arg arg_list_
        """
        return self.defaultNodeClass(
            target='arg_list_',
            option=option,
            names=names,
            values=values)

    def on_arg(self, target, option, names, values):
        """
        arg
            : type ID
        """
        return self.defaultNodeClass(
            target='arg',
            option=option,
            names=names,
            values=values)

    def on_declaration(self, target, option, names, values):
        """
        declaration
            : type ident_list PCOMMA
        """
        return self.defaultNodeClass(
            target='declaration',
            option=option,
            names=names,
            values=values)

    def on_type(self, target, option, names, values):
        """
        type
            : INT
            | FLOAT
            | CHAR
        """
        return self.defaultNodeClass(
            target='type',
            option=option,
            names=names,
            values=values)

    def on_ident_list(self, target, option, names, values):
        """
        ident_list
            : ID ident_list_
        """
        return self.defaultNodeClass(
            target='ident_list',
            option=option,
            names=names,
            values=values)

    def on_ident_list_(self, target, option, names, values):
        """
        ident_list_
            : COMMA ident_list
        """
        return self.defaultNodeClass(
            target='ident_list_',
            option=option,
            names=names,
            values=values)

    def on_stmt(self, target, option, names, values):
        """
        stmt
            : for_stmt
            | while_stmt
            | expr PCOMMA
            | if_stmt
            | compound_stmt
            | declaration
            | PCOMMA
        """
        return self.defaultNodeClass(
            target='stmt',
            option=option,
            names=names,
            values=values)

    def on_for_stmt(self, target, option, names, values):
        """
        for_stmt
            : FOR LBRACKET expr PCOMMA opt_expr PCOMMA opt_expr RBRACKET stmt
        """
        return self.defaultNodeClass(
            target='for_stmt',
            option=option,
            names=names,
            values=values)

    def on_opt_expr(self, target, option, names, values):
        """
        opt_expr
            : expr
        """
        return self.defaultNodeClass(
            target='opt_expr',
            option=option,
            names=names,
            values=values)

    def on_while_stmt(self, target, option, names, values):
        """
        while_stmt
            : WHILE LBRACKET expr RBRACKET stmt
        """
        return self.defaultNodeClass(
            target='while_stmt',
            option=option,
            names=names,
            values=values)

    def on_if_stmt(self, target, option, names, values):
        """
        if_stmt
            : IF LBRACKET expr RBRACKET stmt else_part
        """
        return self.defaultNodeClass(
            target='if_stmt',
            option=option,
            names=names,
            values=values)

    def on_else_part(self, target, option, names, values):
        """
        else_part
            : ELSE stmt
        """
        return self.defaultNodeClass(
            target='else_part',
            option=option,
            names=names,
            values=values)

    def on_compound_stmt(self, target, option, names, values):
        """
        compound_stmt
            : LBRACE stmt_list RBRACE
        """
        return self.defaultNodeClass(
            target='compound_stmt',
            option=option,
            names=names,
            values=values)

    def on_stmt_list(self, target, option, names, values):
        """
        stmt_list
            : stmt stmt_list
            | function stmt_list
        """
        return self.defaultNodeClass(
            target='stmt_list',
            option=option,
            names=names,
            values=values)

    def on_expr(self, target, option, names, values):
        """
        expr
            : ID ATTR expr
            | r_value
        """
        return self.defaultNodeClass(
            target='expr',
            option=option,
            names=names,
            values=values)

    def on_r_value(self, target, option, names, values):
        """
        r_value
            : mag r_value_
        """
        return self.defaultNodeClass(
            target='r_value',
            option=option,
            names=names,
            values=values)

    def on_r_value_(self, target, option, names, values):
        """
        r_value_
            : compare mag r_value_
        """
        return self.defaultNodeClass(
            target='r_value_',
            option=option,
            names=names,
            values=values)

    def on_compare(self, target, option, names, values):
        """
        compare
            : EQ
            | LT
            | GT
            | LE
            | GE
            | NE
        """
        return self.defaultNodeClass(
            target='compare',
            option=option,
            names=names,
            values=values)

    def on_mag(self, target, option, names, values):
        """
        mag
            : term mag_
        """
        return self.defaultNodeClass(
            target='mag',
            option=option,
            names=names,
            values=values)

    def on_mag_(self, target, option, names, values):
        """
        mag_
            : PLUS term mag_
            | MINUS term mag_
        """
        return self.defaultNodeClass(
            target='mag_',
            option=option,
            names=names,
            values=values)

    def on_term(self, target, option, names, values):
        """
        term
            : factor term_
        """
        return self.defaultNodeClass(
            target='term',
            option=option,
            names=names,
            values=values)

    def on_term_(self, target, option, names, values):
        """
        term_
            : MULT factor term_
            | DIV factor term_
        """
        return self.defaultNodeClass(
            target='term_',
            option=option,
            names=names,
            values=values)

    def on_factor(self, target, option, names, values):
        """
        factor
            : LBRACKET expr RBRACKET
            | MINUS factor
            | PLUS factor
            | ID
            | NUMBER
            | CHAR
        """
        return self.defaultNodeClass(
            target='factor',
            option=option,
            names=names,
            values=values)

    # -----------------------------------------
    # raw lex script, verbatim here
    # -----------------------------------------
    lexscript = r"""
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
    """
    # -----------------------------------------
    # end raw lex script
    # -----------------------------------------


def usage():
    print('%s: PyBison parser derived from %s and %s' % (sys.argv[0], bisonFile, lexFile))
    print('Usage: %s [-k] [-v] [-d] [filename]' % sys.argv[0])
    print('  -k       Keep temporary files used in building parse engine lib')
    print('  -v       Enable verbose messages while parser is running')
    print('  -d       Enable garrulous debug messages from parser engine')
    print('  filename path of a file to parse, defaults to stdin')


def main(*args):
    """
    Unit-testing func
    """

    keepfiles = 0
    verbose = 0
    debug = 0
    filename = None
    args = list(args)
    for s in ['-h', '-help', '--h', '--help', '-?']:
        if s in args:
            usage()
            sys.exit(0)

    if len(args) > 0:
        if '-k' in args:
            keepfiles = 1
            args.remove('-k')
        if '-v' in args:
            verbose = 1
            args.remove('-v')
        if '-d' in args:
            debug = 1
            args.remove('-d')
    if len(args) > 0:
        filename = args[0]

    p = Parser(verbose=verbose, keepfiles=keepfiles)
    tree = p.run(file=filename, debug=debug)
    return tree


if __name__ == '__main__':
    main(*(sys.argv[1:]))

