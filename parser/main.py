from parser_data import *
from bnf import *

simple_input = [
 ['int', 'int', 1], 
 ['identifier', 'main', 2],
 ['(', '(', 3],
 [')', ')', 4], 
 ['{', '{', 5],
 ['int', 'int', 6],
 ['identifier', 'a', 7],
 ['=', '=', 8],
 ['number', '5', 9],
 [';', ';', 10],
 ['$', '$', 11]
]



def parser(scanner_output):
    pile = ['$']
    pile.extend(bnf_rules[0][::-1])
    print(pile)

    for i in range(len(scanner_output)):
        while pile[-1] != '$' and scanner_output[i] != '$':
            if (pile[-1] in terminals) and (pile[-1] == scanner_output[i][0]):
                # match();
                pile.pop()
                print(pile)
                i = i+1
            else:
                print('table['+pile[-1]+']['+scanner_output[i][0]+']')
                aux = table[pile[-1]][scanner_output[i][0]]
                print(aux)
                if (pile[-1] not in terminals) and (aux != None):
                    # producao()
                    pile.pop()
                    print(aux[0])
                    pile.extend(bnf_rules[aux[0]-1][::-1])
                    print(pile)
                else:
                    print('Erro na linha ' + str(scanner_output[3]))
                    break
        if pile[-1] == '$' and scanner_output[i] == '$':
            print('arvore')
        else:
            print('Erro na linha ' + str(scanner_output[3]))
            break


parser(simple_input)

