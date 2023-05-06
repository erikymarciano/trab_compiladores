from enum import Enum
import re

class Token_Types(Enum):
    NONE = 'NONE'
    INVALID = 'INVALIDO'
    QUERY = '?-'
    ATRIB = '::='
    PREDICATE = ':-'
    PIPE = '|'
    DOT = '.'
    COMMA = ','
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    ATOM = 'ATOM'
    NUMERAL_INT = 'NUMERAL_INT'
    NUMERAL_FLOAT = 'NUMERAL_FLOAT'
    VARIABLE = 'VARIABLE'
    TOKEN_SEPARATOR = 'TOKEN_SEPARATOR'


#open text file in read mode
text_file = open('./code.txt', 'r')
 
#read whole file to a string
data = text_file.read()
 
#close file
text_file.close()
 
tokens_tuple = []
TOKENS_TO_FILTER = ['\n', ' ', '']



valid_token_type = Token_Types.INVALID
valid_token = ''
possible_token = ''
error_message_format =  "Error reading token '{}' at char {}"
error_message = ''

def compare_regex(token: str, pattern: str,):
    matcher = re.compile(pattern)
    match = matcher.match(token)
    return match != None and match.start() == 0


def get_token_type(token: str) -> Token_Types:
    if token == '':
        return Token_Types.NONE
    
    if token.strip() == '':
        return Token_Types.TOKEN_SEPARATOR
    
    if '?-'.startswith(token):
        return Token_Types.QUERY
    
    if ':-'.startswith(token):
        return Token_Types.PREDICATE
    
    if '::='.startswith(token):
        return Token_Types.ATRIB
    
    if token == '|':
        return Token_Types.PIPE
    
    if token == '.':
        return Token_Types.DOT
    
    if token == ',':
        return Token_Types.COMMA
    
    if token == '(':
        return Token_Types.OPEN_PAREN
    
    if token == ')':
        return Token_Types.CLOSE_PAREN
    
    if compare_regex(token, '^[a-z]+[a-zA-Z0-9_]*$'):
        return Token_Types.ATOM
    
    if compare_regex(token, '^[A-Z_]+[a-zA-Z0-9_]*$'):
        return Token_Types.VARIABLE
    
    # deveria ter um token para os operadores 
    
    if compare_regex(token, '^[-+]?\d+([eE][+-]?)?[\d+]?$'):
        return Token_Types.NUMERAL_INT
    
    if compare_regex(token, '^[-+]?\d+[\.]?[\d+]?([eE][-+]?)?[\d+]?$'):
        return Token_Types.NUMERAL_FLOAT
    
    return Token_Types.INVALID


def try_add_token(token: str) -> bool:
    global valid_token
    global possible_token
    global valid_token_type
    token_type = get_token_type(token)
    if token_type == Token_Types.INVALID:
        return False
    tokens_tuple.append((token, token_type.value))
    valid_token = possible_token = ''
    valid_token_type = None
    return True


# Verifica se existe um caminho válido no automato para este token
def can_be_a_valid_token(token: str) -> bool:
    return get_token_type(token) != Token_Types.INVALID


# Verifica se a posição atual do automato é estado final de um separador
def is_separator_char(char: str) -> bool:
    return char in TOKENS_TO_FILTER


data_pos = 0
data_len = len(data)
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
