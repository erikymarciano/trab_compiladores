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

input_2 = [
 ['int', 'int', 1],
 ['identifier', 'main', 2],
 ['(', '(', 3],
 ['float', 'float', 4],
 ['identifier', 'param1', 5],
 [',', ',', 6],
 ['int', 'int', 7],
 ['identifier', 'param2', 8],
 [')', ')', 9],
 ['{', '{', 10],
 ['int', 'int', 11],
 ['identifier', 'hello', 12],
 [';', ';', 13],
 ['int', 'int', 14],
 ['identifier', 'i', 15],
 [';', ';', 16],
 ['float', 'float', 17],
 ['identifier', 'result', 18],
 [';', ';', 19],
 ['}', '}', 20],
 ['$', '$', 21]
]



def parser(scanner_output):
    pile = ['$']
    pile.extend(bnf_rules[0][::-1])
    print(pile)
    for i in range(len(scanner_output)):
        while pile[-1] != '$' and scanner_output[i] != '$':
            if (pile[-1] == 'ε'):
                pile.pop()
                print(pile)
            else:
                print('Topo da pilha: '+pile[-1])
                print('Token atual: '+scanner_output[i][0])
                if (pile[-1] in terminals) and (pile[-1] == scanner_output[i][0]):
                    # match();
                    pile.pop()
                    print(pile)
                    i = i+1
                else:
                    aux = table[pile[-1]][scanner_output[i][0]]
                    if (len(aux) == 1):
                        if (pile[-1] not in terminals) and (aux != None):
                            # producao()
                            pile.pop()
                            pile.extend(bnf_rules[aux[0]-1][::-1])
                            print(pile)
                        else:
                            print('Erro na linha ' + str(scanner_output[3]))
                            break
                    else:
                        print('Backtracking')
        if (pile[-1] == '$') and (scanner_output[i][0] == '$'):
            print('arvore')
            break
        else:
            print('Erro na linha ' + str(scanner_output[3]))
            break


parser(input_2)

