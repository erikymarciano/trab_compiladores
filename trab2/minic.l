D			[0-9]
L			[a-zA-Z_]


%{

    /* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */

    void count();
    #include <stdio.h>
    #include <string.h>
    #include "minic.tab.h"
    int cur_funcID = 1, id_counter = 1;
    int func_declaration = 0;
    int scope_counter = 0;

    typedef struct node {
	    int NodeID;
	    char ID[10], DataType[10];
        int Scope;
        int IsFunc;
	    struct node *next;
    } node_t;

    node_t*head = NULL, *temp=NULL, *current=NULL;
%}


%%
"int"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
        head->NodeID = id_counter++;
		strcpy(head->DataType, yytext);
        head->Scope = scope_counter;
	} else{
		if (temp == NULL){
			temp = (struct node*)malloc(sizeof(struct node)); 
            temp->NodeID = id_counter++;
			head->next = temp;
		}
		else if (temp->next == NULL) {
			temp->next=(struct node*)malloc(sizeof(struct node)); 
            temp->next->NodeID = id_counter++;
			temp = (node_t*)temp->next;
		}else{
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
            temp->NodeID = id_counter++;
			head->next = temp;
		}
		else if (temp->next == NULL) {
			temp->next=(struct node*)malloc(sizeof(struct node)); 
            temp->next->NodeID = id_counter++;
			temp = (node_t*)temp->next;
		}else{
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
            temp->NodeID = id_counter++;
			head->next = temp;
		}
		else if (temp->next == NULL) {
			temp->next=(struct node*)malloc(sizeof(struct node)); 
            temp->next->NodeID = id_counter++;
			temp = (node_t*)temp->next;
		}else{
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
        head->Scope = scope_counter;
        head->IsFunc = func_declaration;
	} else if (temp->next == NULL){
		strcpy(temp->ID, yytext);
        temp->Scope = scope_counter;
        temp->IsFunc = func_declaration;
	} else{
		temp = (node_t*)temp->next;
		strcpy(temp->ID, yytext);
        temp->Scope = scope_counter;
        temp->IsFunc = func_declaration;
	}
    
    if (func_declaration){
        if (head->next == NULL) {
            cur_funcID = head->NodeID;
        }
        else {
            cur_funcID = temp->NodeID;
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
","			{ 
	if(temp == NULL){
		temp = (struct node*)malloc(sizeof(struct node)); 
        temp->NodeID = id_counter++;
		head->next = temp;
		strcpy(temp->DataType, head->DataType);
	} else {
		temp->next=(struct node*)malloc(sizeof(struct node)); 
        temp->next->NodeID = id_counter++;
		strcpy(temp->next->DataType, temp->DataType);
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
    printf("#\tID\tFUNC\tTYPE\tSCOPE_ID\n");
	while(current!=NULL){
		printf("%d\t%s\t%d\t%s\t%d\n", current->NodeID, current->ID, current->IsFunc, current->DataType, current->Scope);
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
