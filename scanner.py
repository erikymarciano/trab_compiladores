import re
from copy import deepcopy as clone
from collections import defaultdict

#region classes

def subtract_list(listA:list, listB:list) -> list:
    return [o for o in listA if o not in listB]


class Token:
    def __init__(self, nome:str, token:str, exp:str) -> None:
        self.nome = nome
        self.token = self.treat_token(token)
        self.exp = exp
    
    def __str__(self) -> str:
        return "Token '{}':  {}".format(self.nome, self.token)
    
    def treat_token(self, token:str) -> str:
        if token.startswith('\\'):
            return token[1:]
        return token
    

class Rule:
    def __init__(self, from_stage_id:int, to_stage_id:int, exp:str) -> None:
        self.from_id = from_stage_id
        self.to_id = to_stage_id
        self.exp = exp
        
    def __str__(self) -> str:
        return '{} -> {} : {}'.format(self.from_id, self.to_id, self.exp)


class Automata:
    def __init__(self, token:Token, start_stage:int) -> None:
        self.token = token
        self.rules = []
        self.final_stages = []
        self.start_stage = self.current_stage = start_stage
        self.paused = False
        self.steps = 0
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
    
    def at_final_stage(self) -> bool:
        return self.current_stage in self.final_stages
    
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
        self.steps = 0
    

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
    
    def move_reading(self, term:str) -> bool:
        r = self.can_move(term)
        if r:
            self.current_stage = r.to_id
            self.steps += 1
            return True
        return False
    
    def can_move(self, term:str) -> Rule:
        if self.paused:
            return None
        for r in self.rules:
            escaped_exp = re.escape(r.exp)
            if r.exp.startswith('\\') or r.exp.startswith('['):
                escaped_exp = r.exp
            matched = re.match(escaped_exp, term)
            if self.current_stage == r.from_id and matched:
                return r
        self.paused = True
        return None
    
#endregion 

rules_file = open('./rules.txt', 'w', encoding="utf-8")
rules_file.close()
types_file = open('./types.txt', 'r', encoding="utf-8")
code_file = open('./code.txt', 'r', encoding="utf-8")
 
DATA_TYPES = types_file.readlines()
INPUT_DATA = code_file.read()
 
types_file.close()
code_file.close()

EPSILON = 'ε'
TOKENS_SEPARATORS = ['\n', ' ', '']
TOKEN_FILE_SEPARATOR = '; '
TOKEN_TYPES = {'INVALID': Token('INVALID', 'INVALID', None)}
UNIQUE_ID: int = 0

#region funções auxiliares para construcao dos automatos

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

#endregion

#region funções auxiliares de manipulação 

def try_get_token(afds:list[AFD]) -> Token:
    steps = max([a.steps for a in afds])
    # verifica se o maior é um estado final
    greatests:list[AFD] = []
    for afd in afds:
        if afd.steps == steps:
            greatests.append(afd)
    
    for greatest in greatests:
        if greatest.at_final_stage():
            return greatest.token
    
    return TOKEN_TYPES['INVALID']


def is_separator_char(char:str) -> bool:
    return char in TOKENS_SEPARATORS


def reset_automates(automates_list:list[Automata]) -> None:
    for a in automates_list:
        a.reset()


def extract_types(data_lines:list[str]) -> None:
    print('Reading tokens from file...')
    try:
        reading_comment = False
        reading_separators = False
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
            if line == 'SEPARATORS':
                reading_separators = True
                continue
            if reading_separators:
                if line != 'END SEPARATORS':
                    global TOKENS_SEPARATORS
                    TOKENS_SEPARATORS.extend(list(line.split('; ')))
                else:
                    reading_separators = False
                continue
            first_sep_index = line.find(TOKEN_FILE_SEPARATOR)
            last_sep_index = line.rfind(TOKEN_FILE_SEPARATOR)
            type_name, type_token, type_exp = line[:first_sep_index], line[first_sep_index + len(TOKEN_FILE_SEPARATOR):last_sep_index], line[last_sep_index + len(TOKEN_FILE_SEPARATOR):]
            TOKEN_TYPES[type_name] = Token(type_name, type_token, type_exp)
    except:
        print("Error reading file of types!")
        exit(1)
        
    
def get_input_data_line_index(char_index:int) -> int:
    lines = INPUT_DATA.split('\n')
    global_i = 0
    for i in range(len(lines)):
        global_i += len(lines[i]) + 1
        if char_index < global_i:
            return i + 1
    return -1
    

#endregion


token_automates: list[AFD] = []
extract_types(DATA_TYPES)
for k in TOKEN_TYPES:
    token = TOKEN_TYPES[k]
    if not token.exp:
        continue
    start_stage = UNIQUE_ID
    automata_afn = AFN(token, start_stage)
    end_stage = compute_rule_for_exp(automata_afn, start_stage, token.exp)
    automata_afn.set_final_stages([end_stage])
    automata_afd = AFD(token, start_stage)
    automata_afd._transform_from_afn(automata_afn)
    automata_afd._minimize()
    token_automates.append(automata_afd)
    print('Token Found:\t', token)
    get_next_stage_id()

export_automates(token_automates)
print('Reading program...')


data_pos = 0
data_len = len(INPUT_DATA)
token_acc = ''
tokens_scanned:list[(str, str, int)] = []
scanner_error_message = ''
scanner_error_format = "Error reading token '{}' at line {}:  Token is invalid!"
while data_pos < data_len:
    char = INPUT_DATA[data_pos]
    
    automates_rule = [a.move_reading(char) for a in token_automates]
    # nenhum automato conseguiu ler o char
    if all(not r for r in automates_rule):
        line_pos = get_input_data_line_index(data_pos)
        # verifica se está lendo ou se é um separador (como: ' ')
        if is_separator_char(char) or is_separator_char(token_acc):
            token_found = try_get_token(token_automates)
            if token_found != TOKEN_TYPES['INVALID']:
                # salva o token valido + posição na entrada
                tokens_scanned.append((token_found.token, token_acc, line_pos))
                token_acc = ''
                reset_automates(token_automates)
                continue
        if not is_separator_char(char):
            # throw invalid token error
            token_acc += char
            scanner_error_message = scanner_error_format.format(token_acc, line_pos)
            break
        
        # reset to read next token 
        token_acc = char = ''
        reset_automates(token_automates)
    
    token_acc += char
    data_pos += 1
    

print('Printing scanned tokens...')
output = open('./scanner_output.txt', 'w', encoding="utf-8")
for tuple in tokens_scanned:
    output.writelines(str(list(tuple)) + '\n')
output.writelines(str(['$', '$', get_input_data_line_index(data_len)]))
output.close()

if scanner_error_message:
    print(scanner_error_message)
