D			[0-9]
L			[a-zA-Z_]


%{

/* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */

void count();
#include <stdio.h>
#include <string.h>
#include "minic.tab.h"
typedef struct node {
	int NodeID;
	char ID[10], DataType[10];
	struct node *next;
} node_t;

node_t*head = NULL, *temp=NULL, *current=NULL;
%}


%%
"int"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
		strcpy(head->DataType, yytext);
	} else{
		if (temp == NULL){
			temp = (struct node*)malloc(sizeof(struct node));
			head->next = temp;
		}
		else {
			temp->next=(struct node*)malloc(sizeof(struct node));
			temp = (node_t*)temp->next;
		}
		strcpy(temp->DataType, yytext);
	}
	count(); 
	return INT; 
}
"float"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
		strcpy(head->DataType, yytext);
	} else{
		if (temp == NULL){
			temp = (struct node*)malloc(sizeof(struct node));
			head->next = temp;
		}
		else {
			temp->next=(struct node*)malloc(sizeof(struct node));
			temp = (node_t*)temp->next;
		}
		strcpy(temp->DataType, yytext);
	}
	count(); 
	return FLOAT; 
}
"char"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
		strcpy(head->DataType, yytext);
	} else{
		if (temp == NULL){
			temp = (struct node*)malloc(sizeof(struct node));
			head->next = temp;
		}
		else {
			temp->next=(struct node*)malloc(sizeof(struct node));
			temp = (node_t*)temp->next;
		}
		strcpy(temp->DataType, yytext);
	}
	count(); 
	return CHAR; 
}
"if"			{ count(); return IF; }
"else"			{ count(); return ELSE; }
"while"			{ count(); return WHILE; }
"for"			{ count(); return FOR; }

{L}({L}|{D})*	{
	if(head->next == NULL){
		strcpy(head->ID, yytext);
		head->next = NULL;
	} else{
		strcpy(temp->ID, yytext);
		temp->next = NULL;
	}
	count();
	return ID; 
}

{D}+("."{D})*	{ count(); return NUMBER; }

"<="			{ count(); return LE; }
">="			{ count(); return GE; }
"=="			{ count(); return EQ; }
"!="			{ count(); return NE; }
";"			{ 
	if(temp==NULL){
		temp=(struct node*)malloc(sizeof(struct node));
		head->next=temp;
	} else {
		temp->next=(struct node*)malloc(sizeof(struct node));
		temp = (node_t*)temp->next;
	}
	count(); 
	return PCOMMA; 
	}
"{"		{ count(); return LBRACE; }
"}"		{ count(); return RBRACE; }
","			{ 
	if(temp == NULL){
		temp = (struct node*)malloc(sizeof(struct node));
		head->next = temp;
		strcpy(temp->DataType, head->DataType);
	} else if(yytext != ","){
		temp->next=(struct node*)malloc(sizeof(struct node));
		temp = (node_t*)temp->next;		
		strcpy(temp->DataType, yytext);
	}
	
	count(); 
	return COMMA; 
}
"="			{ count(); return ATTR; }
"("			{ count(); return LBRACKET; }
")"			{ count(); return RBRACKET; }
"-"			{ count(); return MINUS; }
"+"			{ count(); return PLUS; }
"*"			{ count(); return MULT; }
"/"			{ count(); return DIV; }
"<"			{ count(); return LT; }
">"			{ count(); return GT; }

[ \t\v\f]		{ count(); }

.			{ /* ignore bad characters */ }

"\n" {
	node_t *current = head;
	while(current!=NULL){
		printf("%s\t%s\n", current->ID, current->DataType);
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
}
