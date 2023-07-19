D			[0-9]
L			[a-zA-Z_]
C           [a-zA-Z0-9]


%{

    void count();
    int getScopeLevel(int id);
    int getScopeFatherId(int id);
    int isIdAtScope(int id, int scope, int is_declaration);
    int getIdAtScope(char *id_name, int id, int is_declaration);
    int getTypeAtScope(char *name, int scope_id);
    void handleIdNameAtScope(char *id_name, int id, int is_declaration);
    void checkSameTypeAtArithmetic(int type1, int type2, char *op);
    void checkSameTypeAtComparison(int type1, int type2, char *op);

    #include <stdio.h>
    #include <string.h>
    #include "minic.tab.h"
    int cur_funcID = 1, id_counter = 1;
    int func_declaration = 0, id_declaration = 0;
    int scope_counter = 0, scope_father = 0;

    typedef struct node {
	    int NodeID;
        int TypeID;
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
        head->TypeID = INT;
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
        temp->TypeID = INT;
	}

    yylval.type = INT;
    yylval.code = "int";
	count(); 
	return INT; 
}
"float"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t)); 
        head->NodeID = id_counter++;
		strcpy(head->DataType, yytext);
        head->TypeID = FLOAT;
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
        temp->TypeID = FLOAT;
	}

    yylval.type = FLOAT;
    yylval.code = "float";
	count(); 
	return FLOAT; 
}
"char"			{ 
	if(head == NULL){
		head = (node_t*) malloc(sizeof(node_t));
        head->NodeID = id_counter++; 
		strcpy(head->DataType, yytext);
        head->TypeID = CHAR;
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
        temp->TypeID = CHAR;
	}
    
    yylval.type = CHAR;
    yylval.code = "char";
	count(); 
	return CHAR; 
}
"if"			{ 
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
    temp->TypeID = IF;
    temp->IsFunc = 2;
    strcpy(temp->ID, yytext);
    cur_funcID = temp->NodeID;
    temp->ScopeFather = scope_father;
    temp->ScopeLevel = scope_counter;

    count(); 
    yylval.type = IF; 
    yylval.code = "if"; 
    return IF; 
}
"else"			{ 
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
    temp->TypeID = ELSE;
    temp->IsFunc = 2;
    strcpy(temp->ID, yytext);
    cur_funcID = temp->NodeID;
    temp->ScopeFather = scope_father;
    temp->ScopeLevel = scope_counter;

    count(); 
    yylval.type = ELSE; 
    yylval.code = "else"; 
    return ELSE; 
}
"while"			{ 
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
    temp->TypeID = WHILE;
    temp->IsFunc = 2;
    strcpy(temp->ID, yytext);
    cur_funcID = temp->NodeID;
    temp->ScopeFather = scope_father;
    temp->ScopeLevel = scope_counter;

    count(); 
    yylval.type = WHILE; 
    yylval.code = "while"; 
    return WHILE; 
}
"for"			{ 
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
    temp->TypeID = FOR;
    temp->IsFunc = 2;
    strcpy(temp->ID, yytext);
    cur_funcID = temp->NodeID;
    temp->ScopeFather = scope_father;
    temp->ScopeLevel = scope_counter;

    count(); 
    yylval.type = FOR; 
    yylval.code = "for"; 
    return FOR; 
}

"'"."'" { 
    count(); 
    yylval.type = CHARACTER; 
    yylval.code = malloc(sizeof *yylval.code *(strlen(yytext)+1)); 
    strcpy(yylval.code, yytext); 
    return CHARACTER; 
}

{L}({L}|{D})*	{

    
    char *thisID = malloc(sizeof *thisID *(strlen(yytext)+1));
    strcpy(thisID, yytext); 

    if (head->next == NULL)
        handleIdNameAtScope(thisID, cur_funcID, (id_declaration + func_declaration) > 0);
    else
        handleIdNameAtScope(thisID, cur_funcID, (id_declaration + func_declaration) > 0);

    if (id_declaration || func_declaration){
	    if(head->next == NULL){
		    strcpy(head->ID, yytext);
            head->ScopeFather = scope_father;
            head->ScopeLevel = scope_counter;
            head->IsFunc = func_declaration;
            
	    } else if (temp->next == NULL){
		    strcpy(temp->ID, yytext);
            temp->ScopeFather = scope_father;
            temp->ScopeLevel = scope_counter;
            temp->IsFunc = func_declaration;
	    } else{
		    temp = (node_t*)temp->next;
		    strcpy(temp->ID, yytext);
            temp->ScopeFather = scope_father;
            temp->ScopeLevel = scope_counter;
            temp->IsFunc = func_declaration;
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
    
    yylval.type = ID; 
    yylval.code = malloc(sizeof *yylval.code *(strlen(yytext)+1));
    strcpy(yylval.code,yytext); 
	count();
	return ID; 
}

{D}+("."{D}+)*	{ 
    count(); 
    yylval.type = NUMBER;  
    yylval.code = malloc(sizeof *yylval.code *(strlen(yytext)+1));
    strcpy(yylval.code, yytext); 
    return NUMBER; 
}

"<="			{ count(); yylval.type = LE; yylval.code = "<="; return LE; }
">="			{ count(); yylval.type = GE; yylval.code = ">="; return GE; }
"=="			{ count(); yylval.type = EQ; yylval.code = "=="; return EQ; }
"!="			{ count(); yylval.type = NE; yylval.code = "!="; return NE; }
";"			{ count(); yylval.type = PCOMMA; yylval.code = ";"; return PCOMMA; }
"{"		{ count(); yylval.type = LBRACE; yylval.code = "{"; return LBRACE; }
"}"		{ count(); yylval.type = RBRACE; yylval.code = "}"; return RBRACE; }
","			{ 
	if(temp == NULL){
		temp = (struct node*)malloc(sizeof(struct node)); 
        temp->NodeID = id_counter++;
		head->next = temp;
		strcpy(temp->DataType, head->DataType);
        temp->TypeID = head->TypeID;
	} else {
		temp->next=(struct node*)malloc(sizeof(struct node)); 
        temp->next->NodeID = id_counter++;
		strcpy(temp->next->DataType, temp->DataType);
        temp->next->TypeID = temp->TypeID;
	}
	
    yylval.type = COMMA; 
    yylval.code = ","; 
	count(); 
	return COMMA; 
}
"="			{ count(); yylval.type = ATTR; yylval.code = "="; return ATTR; }
"("			{ count(); yylval.type = LBRACKET; yylval.code = "("; return LBRACKET; }
")"			{ count(); yylval.type = RBRACKET; yylval.code = ")"; return RBRACKET; }
"-"			{ count(); yylval.type = MINUS; yylval.code = "-"; return MINUS; }
"+"			{ count(); yylval.type = PLUS; yylval.code = "+"; return PLUS; }
"*"			{ count(); yylval.type = MULT; yylval.code = "*"; return MULT; }
"/"			{ count(); yylval.type = DIV; yylval.code = "/"; return DIV; }
"<"			{ count(); yylval.type = LT; yylval.code = "<"; return LT; }
">"			{ count(); yylval.type = GT; yylval.code = ">"; return GT; }

[ \t\v\f\n]		{ count(); }

.			{  }

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
int line = 1;

void count()
{
	int i;

	for (i = 0; yytext[i] != '\0'; i++)
		if (yytext[i] == '\n'){
			column = 0;
			line++;
		}
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


int isIdAtScope(int id, int scope, int is_declaration){
    //printf("isIdAtScope %d  %d = ", id, scope);
    int level1 = getScopeLevel(id);
    int level2 = getScopeLevel(scope);
    if (level1 > level2){
        for(int i = level2; i < level1; i++){
            id = getScopeFatherId(id);
        }
    } else if (level2 > level1){
        for(int i = level1; i < level2; i++){
            scope = getScopeFatherId(scope);
        }
    }

    if (getScopeFatherId(id) == getScopeFatherId(scope)){
        //printf("%d\n", id == scope);
        return id == scope; 
    }
    //printf("%d\n", getScopeFatherId(id) == getScopeFatherId(scope));
    return getScopeFatherId(id) == getScopeFatherId(scope);
}


int getIdAtScope(char *id_name, int id, int is_declaration){
    // busca na tabela de simbolos se ja existe esse identificador neste escopo
    node_t *current = head;
	while(current != NULL){
        if ((strcmp(current->ID, id_name) == 0) && isIdAtScope(current->NodeID, id, is_declaration)) return current->NodeID;
		current = current->next;
	}
	return -1;
}

int getTypeAtScope(char *name, int scope_id){
    node_t *current = head;
	while(current != NULL){
        if ((strcmp(current->ID, name) == 0) && current->ScopeFather == scope_id) return current->TypeID;
		current = current->next;
	}
    return -1;
}

void handleIdNameAtScope(char *id_name, int id, int is_declaration){
    if((getIdAtScope(id_name, id, is_declaration) > 0) && is_declaration)
        printf("[Error] line %d column %d - Identificador %s declarado anteriormente\n", line, column, id_name);

    else if((getIdAtScope(id_name, id, is_declaration) <= 0) && !is_declaration)
        printf("[Error] line %d column %d - Identificador %s não foi declarado\n", line, column, id_name);
}

void checkSameTypeAtArithmetic(int type1, int type2, char *op){
    //operação aritmetica apenas com numbers. Não aceita char
    if (type1 != CHAR && type1 != CHARACTER && type2 != CHAR && type2 != CHARACTER)
        return;
    
    printf("[Error] line %d column %d - Tipos não compatíveis para operação \"%s\"\n", line, column, op);
}

void checkSameTypeAtComparison(int type1, int type2, char *op){
    //comparaçoes entre numbers ou entre characs
    if (type1 != CHAR && type1 != CHARACTER && type2 != CHAR && type2 != CHARACTER)
        return;

    if ((type1 == CHAR || type1 == CHARACTER) && (type2 == CHAR || type2 == CHARACTER))
        return;
    
    printf("[Error] line %d column %d - Tipos não compatíveis para comparação \"%s\"\n", line, column, op);
}
