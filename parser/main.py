from parser_data import *

simple_input = [
 ['int', 'int'], 
 ['identifier', 'main'],
 ['(', '('],
 [')', ')'], 
 ['{', '{'],
 ['int', 'int'],
 ['identifier', 'a'],
 ['='],
 ['number', '5'],
 [';', ';']
]

pile = []
pile.extend(bnf_rules[0][::-1])

for token in simple_input:
    if pile[-1] not in terminals:
        aux = pile[-1]
        pile.pop()
        pile.extend()
    elif token == pile[-1]:
        continue
    else:
        print('Erro na linha x')

