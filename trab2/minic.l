D			[0-9]
L			[a-zA-Z_]


%{

/* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */

void count();
#include <stdio.h>
#include <string.h>
#include "minic.tab.h"
#define MAXTOKENLEN 45

typedef struct node {
	int NodeID, IsFunction;
	char ID[MAXTOKENLEN], DataType[MAXTOKENLEN];
	struct node *next;
} node_t;

node_t*head = NULL, *temp=NULL, *current=NULL;
char LastDT[MAXTOKENLEN];
int isDeclaration;
int isFunction = 1;
%}


%%
"int"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
		strcpy(head->DataType, yytext);
		head->NodeID = 1;
		head->IsFunction = isFunction;
	} else{
		strcpy(temp->DataType, yytext);
	}
	strcpy(LastDT, yytext);
	count(); 
	isDeclaration = 1;
	return INT; 
}
"float"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
		strcpy(head->DataType, yytext);
		head->NodeID = 1;
		head->IsFunction = isFunction;
	} else{
		strcpy(temp->DataType, yytext);
	}
	strcpy(LastDT, yytext);
	count(); 
	isDeclaration = 1;
	return FLOAT; 
}
"char"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
		strcpy(head->DataType, yytext);
		head->NodeID = 1;
		head->IsFunction = isFunction;
	} else{
		strcpy(temp->DataType, yytext);
	}
	strcpy(LastDT, yytext);
	count(); 
	isDeclaration = 1;
	return CHAR; 
}
"if"			{ count(); return IF; }
"else"			{ count(); return ELSE; }
"while"			{ count(); return WHILE; }
"for"			{ count(); return FOR; }

{L}({L}|{D})*	{
	if(head->next == NULL){
		strcpy(head->ID, yytext);
		temp = (struct node*)malloc(sizeof(struct node));
		head->next = temp;
		temp->NodeID = head->NodeID + 1;
	} else if (isDeclaration){
		strcpy(temp->ID, yytext);
		if (temp->DataType[0] == NULL){
			strcpy(temp->DataType, LastDT);
		}
		if (temp->next == NULL){
			temp->next = (struct node*)malloc(sizeof(struct node));
			temp->next->NodeID = temp->NodeID + 1;
			temp = (node_t*)temp->next;
		}
	}
	count();
	return ID; 
}

{D}+("."{D})*	{ count(); return NUMBER; }

"<="			{ count(); return LE; }
">="			{ count(); return GE; }
"=="			{ count(); return EQ; }
"!="			{ count(); return NE; }
";"			{ count(); return PCOMMA; }
"{"		{ count(); return LBRACE; }
"}"		{ count(); return RBRACE; }
","			{ count(); isDeclaration = 1; return COMMA; }
"="			{ count(); return ATTR; }
"("			{ count(); return LBRACKET; }
")"			{ count(); return RBRACKET; }
"-"			{ count(); return MINUS; }
"+"			{ count(); return PLUS; }
"*"			{ count(); return MULT; }
"/"			{ count(); return DIV; }
"<"			{ count(); return LT; }
">"			{ count();return GT; }

[ \t\v\f]		{ int tempDeclaration = isDeclaration; count();  isDeclaration = tempDeclaration; }

.			{ /* ignore bad characters */ }

"\n" {
	node_t *current = head;
	printf("|#\t|ID\t|TYPE\t|FUNC\n");
	printf("| \t|  \t|    \t|    \n");
	while(current!=NULL){
		printf("|%d\t|%s\t|%s\t|%d\n",current->NodeID, current->ID, current->DataType, current->IsFunction);
		current = current->next;
	}
}

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

	isDeclaration = 0;
}
