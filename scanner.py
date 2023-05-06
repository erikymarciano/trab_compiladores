import re

class Token:
    def __init__(self, nome:str, token:str, exp:str) -> None:
        self.nome = nome
        self.token = token
        self.exp = exp
    
    def __str__(self) -> str:
        return "Token '{}':  {}".format(self.nome, self.token)
    # INVALID = 'INVALIDO'
    # NONE = 'NONE'
    # QUERY = '?-'
    # ATRIB = '::='
    # PREDICATE = ':-'
    # PIPE = '|'
    # DOT = '.'
    # COMMA = ','
    # OPEN_PAREN = '('
    # CLOSE_PAREN = ')'
    # ATOM = 'ATOM'
    # NUMERAL_INT = 'NUMERAL_INT'
    # NUMERAL_FLOAT = 'NUMERAL_FLOAT'
    # VARIABLE = 'VARIABLE'
    # TOKEN_SEPARATOR = 'TOKEN_SEPARATOR'
    

class Rule:
    def __init__(self, from_stage_id:int, to_stage_id:int, exp:str) -> None:
        self.from_id = from_stage_id
        self.to_id = to_stage_id
        self.exp = exp
        
    def __str__(self) -> str:
        return '{} -> {} : {}'.format(self.from_id, self.to_id, self.exp)
        
    def accepts(self, char:str) -> bool:
        match = re.match(self.exp, char)
        return match != None and match.start() == 0


types_file = open('./types.txt', 'r', encoding="utf-8")
code_file = open('./code.txt', 'r', encoding="utf-8")
rules_file = open('./rules.txt', 'w', encoding="utf-8")
 
data_types = types_file.readlines()
data = code_file.read()
 
types_file.close()
code_file.close()
rules_file.close()
 
tokens_tuple = []
rules = []
TOKENS_TO_FILTER = ['\n', ' ', '']
TOKEN_FILE_SEPARATOR = '; '
TOKEN_TYPES = {'INVALID': Token('INVALID', 'INVALID', None)}
UNIQUE_ID = 0


valid_token_type = TOKEN_TYPES['INVALID']
valid_token = ''
possible_token = ''
error_message_format =  "Error reading token '{}' at char '{}'"
error_message = ''


# Realiza o split do conteudo entre virgulas
def split_pipe_exp(pipe_exp: str) -> list[str]:
    return list(re.split(r'(?<!\\),', pipe_exp))


# Avalia a expressao regular e retorna a instrução mais imediata 
def get_possible_nested(nested_data:str) -> str:
    try:
        acc = ''
        pilha = []
        skip = False
        if nested_data == '':
            return ''
        
        for c in nested_data:
            acc += c
            
            if skip:
                skip = False
                if len(pilha) == 0:
                    return acc
                continue
            
            if c == '\\':
                skip = True
                continue
            
            if c == '(':
                pilha.append(')')
            if c == '[':
                pilha.append(']')
            
            if c == ')':
                popped = pilha.pop()
                if popped != ')':
                    raise
            if c == ']':
                popped = pilha.pop()
                if popped != ']':
                    raise
                
            if acc != '(' and acc != '[' and len(pilha) == 0 and acc:
                return acc #if acc != nested_data else try_remove_nested(acc)
        
        if len(pilha) > 0 or not acc:
            raise
        
        return acc #if acc != nested_data else try_remove_nested(acc)
    except:
        print('Error finding possible nested exp!')
        exit(1)


# Avalia a expressão regular e retorna a proxima instrução sem ser a imediata
def get_next_exp(exp:str) -> str:
    current_exp = get_possible_nested(exp)
    return get_possible_nested(exp[len(current_exp):])


# Obtém o próximo id único de estado
def get_next_stage_id() -> int:
    global UNIQUE_ID
    UNIQUE_ID += 1
    return UNIQUE_ID


# Adiciona mais de uma regra de transição, de um estado para outro
def add_pipe_rule(from_stage:int, to_stage:int, reading_list:list[str]) -> None:
    for reading in reading_list:
        add_rule(from_stage, to_stage, reading)


# Adiciona regra de transição, de um estado para outro, lendo expressão       
def add_rule(from_stage:int, to_stage:int, reading:str) -> None:
    if from_stage == to_stage and not reading:
        return
    
    rule = Rule(from_stage, to_stage, reading)
    rules.append(rule)
    rules_file = open('./rules.txt', 'a', encoding="utf-8")
    rules_file.write(str(rule) + '\n')
    rules_file.close()


# Adiciona quebra de linha para separar automatos de diferentes tokens
def separate_token_rules() -> None:
    rules_file = open('./rules.txt', 'a', encoding="utf-8")
    rules_file.write('\n')
    rules_file.close()


# Vai adicionado as regras de transição do automato conforme vai lendo expressão
def compute_rule_for_exp(current_stage:int, exp:str) -> int:
    try:
        if exp == '':
            return current_stage
        
        current_exp = get_possible_nested(exp)
        next_exp = get_next_exp(exp)
        
        if current_exp == '*':
            end_stage = compute_rule_for_exp(current_stage, next_exp)
            add_rule(end_stage, current_stage, 'ε')
            add_rule(current_stage, end_stage, 'ε')
            return compute_rule_for_exp(end_stage, exp[1 + len(next_exp):])
        
        if current_exp == '+':
            end_stage = compute_rule_for_exp(current_stage, next_exp)
            add_rule(end_stage, current_stage, 'ε')
            return compute_rule_for_exp(end_stage, exp[1 + len(next_exp):])
            
        if current_exp == '|':
            pass
            next_stage = get_next_stage_id()
            add_pipe_rule(current_stage, next_stage, split_pipe_exp(next_exp[1:-1]))
            return compute_rule_for_exp(next_stage, exp[1 + len(next_exp):])
            
        if current_exp.startswith('('):
            current_exp = current_exp[1:-1]
            return compute_rule_for_exp(current_stage, current_exp)
        
        next_stage = get_next_stage_id()
        add_rule(current_stage, next_stage, current_exp)
        return compute_rule_for_exp(next_stage, exp[len(current_exp):])
    except:
        print('Error creating rule!')
        exit(1)




def get_token_type(token: str) -> Token:
    # if token == '':
    #     return Token_Types.NONE
    
    # if token.strip() == '':
    #     return Token_Types.TOKEN_SEPARATOR
    
    # if '?-'.startswith(token):
    #     return Token_Types.QUERY
    
    # if ':-'.startswith(token):
    #     return Token_Types.PREDICATE
    
    # if '::='.startswith(token):
    #     return Token_Types.ATRIB
    
    # if token == '|':
    #     return Token_Types.PIPE
    
    # if token == '.':
    #     return Token_Types.DOT
    
    # if token == ',':
    #     return Token_Types.COMMA
    
    # if token == '(':
    #     return Token_Types.OPEN_PAREN
    
    # if token == ')':
    #     return Token_Types.CLOSE_PAREN
    
    # if compare_regex(token, '^[a-z]+[a-zA-Z0-9_]*$'):
    #     return Token_Types.ATOM
    
    # if compare_regex(token, '^[A-Z_]+[a-zA-Z0-9_]*$'):
    #     return Token_Types.VARIABLE
    
    # # deveria ter um token para os operadores 
    
    # if compare_regex(token, '^[-+]?\d+([eE][+-]?)?[\d+]?$'):
    #     return Token_Types.NUMERAL_INT
    
    # if compare_regex(token, '^[-+]?\d+[\.]?[\d+]?([eE][-+]?)?[\d+]?$'):
    #     return Token_Types.NUMERAL_FLOAT
    
    # return Token_Types.INVALID
    pass


def try_add_token(token: str) -> bool:
    global valid_token
    global possible_token
    global valid_token_type
    token_type = get_token_type(token)
    if token_type == TOKEN_TYPES['INVALID']:
        return False
    tokens_tuple.append((token, token_type.value))
    valid_token = possible_token = ''
    valid_token_type = None
    return True


# Verifica se existe um caminho válido no automato para este token
def can_be_a_valid_token(token: str) -> bool:
    return get_token_type(token) != TOKEN_TYPES['INVALID']


# Verifica se a posição atual do automato é estado final de um separador
def is_separator_char(char: str) -> bool:
    return char in TOKENS_TO_FILTER


def extract_types(data_lines:list[str]) -> None:
    print('Reading tokens from file...')
    try:
        reading_comment = False
        for line in data_lines:
            line = line.strip()
            if not line:
                continue
            if line == 'COMMENT':
                reading_comment = True
                continue
            if reading_comment:
                reading_comment = (line != 'END COMMENT')
                continue
            first_sep_index = line.find(TOKEN_FILE_SEPARATOR)
            last_sep_index = line.rfind(TOKEN_FILE_SEPARATOR)
            type_name, type_token, type_exp = line[:first_sep_index], line[first_sep_index + len(TOKEN_FILE_SEPARATOR):last_sep_index], line[last_sep_index + len(TOKEN_FILE_SEPARATOR):]
            TOKEN_TYPES[type_name] = Token(type_name, type_token, type_exp)
    except:
        print("Error reading file of types!")
        exit(1)


data_pos = 0
data_len = len(data)
extract_types(data_types)
automates_start = []
for k in TOKEN_TYPES:
    token = TOKEN_TYPES[k]
    if not token.exp:
        continue
    start_stage = UNIQUE_ID
    automates_start.append(start_stage)
    compute_rule_for_exp(start_stage, token.exp)
    separate_token_rules()
    print('Token Found:\t', token)
    get_next_stage_id()

print('Reading program...')
exit()
while data_pos < data_len:
    char = data[data_pos]
    data_pos += 1
    
    # if is_separator_char(char):
    #     if valid_token:
    #         has_token_error = try_add_token(valid_token, valid_token_type)
    #         if (has_token_error):
    #             print(error_message.format(valid_token, i))
    #             exit(1)
    #     continue
    
    possible_token += char
    if not can_be_a_valid_token(possible_token):
        if valid_token:
            added_token = try_add_token(valid_token)
            if not added_token:
                error_message = error_message_format.format(possible_token, data_pos)
                break
            data_pos -= 1
        else:
            error_message = error_message_format.format(possible_token, data_pos)
            break
        continue
    valid_token = possible_token



# current_token_type = get_token_type(data, current_token)
# try_add_token(current_token, current_token_type)

for tuple in tokens_tuple:
    print(tuple)

if error_message:
    print(error_message)
