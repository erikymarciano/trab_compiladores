D			[0-9]
L			[a-zA-Z_]


%{

    /* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */

    void count();
    int getScopeLevel(int id);
    int getScopeFatherId(int id);
    int hasSimilarScopes(int id1, int id2);
    int getIdAtScope(char *id_name, int id);
    void handleIdNameAtScope(char *id_name, int id, int is_declaration);
    #include <stdio.h>
    #include <string.h>
    #include "minic.tab.h"
    int cur_funcID = 1, id_counter = 1;
    int func_declaration = 0, id_declaration = 0;
    int scope_counter = 0, scope_father = 0;

    typedef struct node {
	    int NodeID;
	    char ID[32], DataType[10];
        int ScopeFather, ScopeLevel;
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
        head->ScopeFather = scope_father;
        head->ScopeLevel = scope_counter;
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
    if (id_declaration || func_declaration){
	    if(head->next == NULL){
		    strcpy(head->ID, yytext);
            head->ScopeFather = scope_father;
            head->ScopeLevel = scope_counter;
            head->IsFunc = func_declaration;
            handleIdNameAtScope(head->ID, head->NodeID, id_declaration + func_declaration > 0);
            
	    } else if (temp->next == NULL){
		    strcpy(temp->ID, yytext);
            temp->ScopeFather = scope_father;
            temp->ScopeLevel = scope_counter;
            temp->IsFunc = func_declaration;
            handleIdNameAtScope(temp->ID, temp->NodeID, id_declaration + func_declaration > 0);
	    } else{
		    temp = (node_t*)temp->next;
		    strcpy(temp->ID, yytext);
            temp->ScopeFather = scope_father;
            temp->ScopeLevel = scope_counter;
            temp->IsFunc = func_declaration;
            handleIdNameAtScope(temp->ID, temp->NodeID, id_declaration + func_declaration > 0);
	    }
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

[ \t\v\f\n]		{ count(); }

.			{ /* ignore bad characters */ }

<<EOF>> {
    //tabela de simbolos
	node_t *current = head;
    printf("#\tID\tFUNC\tTYPE\tSCOPE_ID\tSCOPE_LEVEL\n");
	while(current != NULL){
		printf("%d\t%s\t%d\t%s\t%d\t\t%d\n", current->NodeID, current->ID, current->IsFunc, current->DataType, current->ScopeFather, current->ScopeLevel);
		current = current->next;
	}
    yyterminate();
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


int getScopeLevel(int id){
node_t *current = head;
	while(current != NULL){
        if (current->NodeID == id) return current->ScopeLevel;
		current = current->next;
	}
	return -1;
}


int getScopeFatherId(int id){
    node_t *current = head;
	while(current != NULL){
        if (current->NodeID == id) return current->ScopeFather;
		current = current->next;
	}
	return -1;
}


int hasSimilarScopes(int id1, int id2){
    int level1 = getScopeLevel(id1);
    int level2 = getScopeLevel(id2);
    if (level1 > level2){
        for(int i = level2; i < level1; i++){
            id1 = getScopeFatherId(id1);
        }
    } else if (level2 > level1){
        for(int i = level1; i < level2; i++){
            id2 = getScopeFatherId(id2);
        }
    }

    if (level1 == 0 || level2 == 0)
        return id1 == id2;
    return getScopeFatherId(id1) == getScopeFatherId(id2); 
}


int getIdAtScope(char *id_name, int id){
    // busca na tabela de simbolos se ja existe esse identificador neste escopo
    node_t *current = head;
	while(current != NULL){
        if (strcmp(current->ID, id_name) == 0 && current->NodeID != id && hasSimilarScopes(current->NodeID, id)) return current->NodeID;
		current = current->next;
	}
	return -1;
}

void handleIdNameAtScope(char *id_name, int id, int is_declaration){
    if(getIdAtScope(id_name, id) > 0 && is_declaration)
        printf("[Error]\tIdentificador %s declarado anteriormente\n", id_name);

    else if(getIdAtScope(id_name, id) <= 0 && !is_declaration)
        printf("[Error]\tIdentificador %s não foi declarado\n", id_name);
}
