import re
from copy import deepcopy as clone
from collections import defaultdict


def subtract_list(listA:list, listB:list) -> list:
    return [o for o in listA if o not in listB]


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


class Automata:
    def __init__(self, start_stage:int) -> None:
        self.rules = []
        self.final_stages = []
        self.start_stage = self.current_stage = start_stage
        self.paused = False
        self.stages = []
        self.terminals = []
        self.get_stages_from_rules()
    
    def __str__(self) -> str:
        out = 'start: {}\n'.format(self.start_stage)
        out += ('\n'.join([str(r) for r in self.rules])) + '\n'
        out += 'finals: {}\n\n'.format(str(self.final_stages))
        return out
    
    def get_stages_from_rules(self) -> None:
        self.stages = []
        for r in self.rules:
            self.add_rules_info(r)
    
    def is_stage_final(self, stage:int) -> bool:
        return stage in self.final_stages
    
    def add_rule(self, rule:Rule) -> None:
        self.rules.append(rule)
        self.add_rules_info(rule)
        
    def add_rules_info(self, rule:Rule) -> None:
        self.stages.append(rule.from_id)
        self.stages.append(rule.to_id)
        if rule.exp != EPSILON:
            self.terminals.append(rule.exp)
        self.stages = list(set(self.stages))
        self.terminals = list(set(self.terminals))
        
    def set_final_stages(self, final_stages:list[int]) -> None:
        self.final_stages = final_stages
        
    def reset(self) -> None:
        self.current_stage = self.start_stage
        self.paused = False
    

class AFN(Automata):
    def _fechamentoE(self, stages:list[int]) -> list[int]:
        stack = []
        res = []
        for st in stages:
            stack.append(st) 
            res.append(st) 
        while stack:
            t = stack.pop()
            for rule in self.rules:
                if rule.from_id == t and rule.exp == EPSILON:
                    u = rule.to_id
                    if u not in res:
                        res.append(u)
                        stack.append(u)
        return list(set(res))
    
    def _move(self, stages:list[int], reading:str) -> list[int]:
        res = []
        for rule in self.rules:
            if rule.from_id in stages and rule.exp == reading:
                res.append(rule.to_id)
        return list(set(res))


class AFD(Automata):
    def _transform_from_afn(self, afn:AFN) -> None:
        self.subsets = {}
        start_subset = str(afn._fechamentoE([afn.start_stage]))
        self.subsets.update({start_subset: self.start_stage})
        Dstage = [(self.start_stage, False)]
        while any(not st[1] for st in Dstage):
            unmarkedIndex = next(i for i, st in enumerate(Dstage) if not st[1])
            Dstage[unmarkedIndex] = (Dstage[unmarkedIndex][0],True)
            t = Dstage[unmarkedIndex][0]
            t_subset = self._get_subset_from_afd_stage(t)
            for term in afn.terminals:
                u = str(afn._fechamentoE(afn._move(t_subset, term)))
                if u == '[]':
                    continue
                if u not in self.subsets:
                    dest_stage = get_next_stage_id()
                    self.subsets.update({u: dest_stage})
                if all(self.subsets[u] != st[0] for st in Dstage):
                    Dstage.append((self.subsets[u], False))
                self.add_rule(Rule(t, self.subsets[u], term))
        
        afd_finals = []
        for subset_key in self.subsets:
            subset = eval(subset_key)
            if any(f in subset for f in afn.final_stages):
                afd_finals.append(self.subsets[subset_key])
        self.final_stages = list(set(afd_finals))
    
    def _move(self, stages:list[int], reading:str) -> int:
        for rule in self.rules:
            if rule.from_id in stages and rule.exp == reading:
                return rule.to_id
        return -1
    
    def _get_subset_from_afd_stage(self, afd_stage:int) -> str:
        for subset_key in self.subsets:
            if self.subsets[subset_key] == afd_stage:
                return eval(subset_key)
        return ''
    
    def _minimize(self) -> None:
        new_pi = self._new_pi([self.final_stages, subtract_list(self.stages, self.final_stages)])
        for g in new_pi:
            for st in g[1:]:
                for r in self.rules.copy():
                    if r.from_id == st:
                        self.rules.remove(r)
                        continue
                    r.to_id = next(value[0] for value in new_pi if r.to_id in value)
        
        self.get_stages_from_rules()
        self.start_stage = next(value[0] for value in new_pi if self.start_stage in value)
        new_finals = []
        for final in self.final_stages:
            new_finals.append(next(value[0] for value in new_pi if final in value))
        self.set_final_stages(new_finals)
    
    def _split_group(self, group:list[int], pi:list[list[int]]) -> list[list[int]]:
        if len(group) < 2:
            return [group]
        dests = []
        for st in group:
            dest_groups = []
            for a in self.terminals:
                dest = self._move([st], a)
                dest_groups.append(next((i for i, value in enumerate(pi) if dest in value), -1))
            dests.append(dest_groups)
        
        groups = defaultdict(list)
        for dst in dests:
            groups[str(dst)].append(dst)
        
        partitions = []
        for g_key in groups:
            part = []
            for i in range(len(dests)):
                if g_key == str(dests[i]):
                    part.append(group[i])
            if part:
                partitions.append(part)
        return partitions
    
    def _new_pi(self, pi:list[list[int]]) -> list[list[int]]:
        while True:
            new_pi = clone(pi)
            for g in pi:
                subgroups = self._split_group(g, pi)
                new_pi.remove(g)
                for sg in subgroups:
                    new_pi.append(sg)
            
            if new_pi == pi:
                break
            pi = new_pi
        return pi
    # def can_move_reading(self, char:str) -> bool:
    #     match = re.match(self.exp, char)
    #     return match != None and match.start() == 0
    


types_file = open('./types.txt', 'r', encoding="utf-8")
code_file = open('./code.txt', 'r', encoding="utf-8")
rules_file = open('./rules.txt', 'w', encoding="utf-8")
 
data_types = types_file.readlines()
data = code_file.read()
 
types_file.close()
code_file.close()
rules_file.close()
 
tokens_tuple = []
automates = []
EPSILON = 'ε'
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
def add_pipe_rule(automata:Automata, from_stage:int, to_stage:int, reading_list:list[str]) -> None:
    for reading in reading_list:
        add_rule_to_automata(automata, from_stage, to_stage, reading)


# Adiciona regra de transição, de um estado para outro, lendo expressão       
def add_rule_to_automata(automata:Automata, from_stage:int, to_stage:int, reading:str) -> None:
    if from_stage == to_stage and not reading:
        return
    
    automata.add_rule(Rule(from_stage, to_stage, reading))


# Vai adicionado as regras de transição do automato conforme vai lendo expressão
def compute_rule_for_exp(automata:Automata, current_stage:int, exp:str) -> int:
    try:
        if exp == '':
            return current_stage
        
        current_exp = get_possible_nested(exp)
        next_exp = get_next_exp(exp)
        
        if current_exp == '*':
            end_stage = compute_rule_for_exp(automata, current_stage, next_exp)
            add_rule_to_automata(automata, end_stage, current_stage, EPSILON)
            add_rule_to_automata(automata, current_stage, end_stage, EPSILON)
            return compute_rule_for_exp(automata, end_stage, exp[1 + len(next_exp):])
        
        if current_exp == '+':
            end_stage = compute_rule_for_exp(automata, current_stage, next_exp)
            add_rule_to_automata(automata, end_stage, current_stage, EPSILON)
            return compute_rule_for_exp(automata, end_stage, exp[1 + len(next_exp):])
            
        if current_exp == '|':
            pass
            next_stage = get_next_stage_id()
            add_pipe_rule(automata, current_stage, next_stage, split_pipe_exp(next_exp[1:-1]))
            return compute_rule_for_exp(automata, next_stage, exp[1 + len(next_exp):])
            
        if current_exp.startswith('('):
            current_exp = current_exp[1:-1]
            return compute_rule_for_exp(automata, current_stage, current_exp)
        
        next_stage = get_next_stage_id()
        add_rule_to_automata(automata, current_stage, next_stage, current_exp)
        return compute_rule_for_exp(automata, next_stage, exp[len(current_exp):])
    except:
        print('Error creating rule!')
        exit(1)


def export_automates(automates:list[Automata]):
    rules_file = open('./rules.txt', 'a', encoding="utf-8")
    for automata in automates:
        rules_file.write(str(automata))        
    rules_file.close()


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
for k in TOKEN_TYPES:
    token = TOKEN_TYPES[k]
    if not token.exp:
        continue
    start_stage = UNIQUE_ID
    automata = Automata(start_stage)
    end_stage = compute_rule_for_exp(automata, start_stage, token.exp)
    automata.set_final_stages([end_stage])
    automates.append(automata)
    print('Token Found:\t', token)
    get_next_stage_id()

export_automates(automates)
print('Reading program...')


dragonAFN = AFN(0)
dragonAFN.add_rule(Rule(0, 1, EPSILON))
dragonAFN.add_rule(Rule(0, 7, EPSILON))
dragonAFN.add_rule(Rule(1, 2, EPSILON))
dragonAFN.add_rule(Rule(1, 4, EPSILON))
dragonAFN.add_rule(Rule(2, 3, 'a'))
dragonAFN.add_rule(Rule(3, 6, EPSILON))
dragonAFN.add_rule(Rule(4, 5, 'b'))
dragonAFN.add_rule(Rule(5, 6, EPSILON))
dragonAFN.add_rule(Rule(6, 1, EPSILON))
dragonAFN.add_rule(Rule(6, 7, EPSILON))
dragonAFN.add_rule(Rule(7, 8, 'a'))
dragonAFN.add_rule(Rule(8, 9, 'b'))
dragonAFN.add_rule(Rule(9, 10, 'b'))
dragonAFN.set_final_stages([10])
print('move: {}'.format(dragonAFN._move([0, 1, 2, 4, 7], 'a')))
print('fechamentoE: {}'.format(dragonAFN._fechamentoE([3, 8])))

dragonAFD = AFD(11)
dragonAFD._transform_from_afn(dragonAFN)
print(dragonAFD)
dragonAFD._minimize()
print(dragonAFD)

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
