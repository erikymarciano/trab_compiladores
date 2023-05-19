from anytree import Node, RenderTree
from copy import deepcopy
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
 ['}', '}', 10],
 ['$', '$', 11]
]

input_4 = [
 ['int', 'int', 1], 
 ['identifier', 'main', 2],
 ['(', '(', 3],
 ['int', 'int', 4],
 ['identifier', 'haha', 5],
 [')', ')', 6], 
 ['{', '{', 7],
 ['int', 'int', 8],
 ['identifier', 'a', 9],
 [';', ';', 12],
 ['identifier', 'a', 9],
 ['=', '=', 10],
 ['number', '5', 11],
 [';', ';', 12],
 ['}', '}', 13],
 ['$', '$', 14]
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
#  ['if', 'if', 11],
#  ['(', '(', 12],
#  ['number', '5', 13],
#  ['==', '==', 13],
#  ['number', '5', 13],
#  [')', ')', 12],
#  [';', ';', 12],
#  ['else', 'else', 12],
#  [';', ';', 12],
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
    derivacao = bnf_rules[0][::-1]
    pile.extend(derivacao)
    print(pile)
    
    pile_backtrack:list[(int, int, list[Node], list[str])] = [] # i_entrada, id_regra, no_pai, estado_lista_nos, estado_da_pilha
    try_backtrack = False
    backtracking_aux = None
    i = 0
    tree = Node("<Function>")
    tree_nodes = []
    for item in derivacao:
        node = Node(item, parent=tree)
        tree_nodes.append(node)
    while(True):
        while pile[-1] != '$' and scanner_output[i] != '$':
            if (pile[-1] == 'ε'):
                pile.pop()
                tree_nodes.pop()
                print(pile)
            else:
                print('Topo da pilha: '+pile[-1])
                print('Token atual: '+scanner_output[i][0])
                if (pile[-1] in terminals) and (pile[-1] == scanner_output[i][0]):
                    # match();
                    node_name = pile.pop()
                    node_parent = tree_nodes.pop()
                    if node_name != node_parent.name:
                        node = Node(node_name, parent=node_parent)
                    print(pile)
                    i = i+1
                else:
                    
                    if backtracking_aux:
                        aux = [backtracking_aux]
                        backtracking_aux = None
                    elif pile[-1] in table.keys() and scanner_output[i][0] in table[pile[-1]].keys():
                        aux = table[pile[-1]][scanner_output[i][0]]
                        for k in range(1, len(aux)):
                            pile_backtrack.append((i + 1, aux[0], deepcopy(tree_nodes), pile.copy()))
                    if (pile[-1] not in terminals) and (aux != None):
                        # producao()
                        node_name = pile.pop()
                        node_parent = tree_nodes.pop()
                        derivacao = bnf_rules[aux[0]-1][::-1]
                        for item in derivacao:
                            node = Node(item, parent=node_parent)
                            tree_nodes.append(node)
                        pile.extend(derivacao)
                        print(pile)
                    else:
                        try_backtrack = True
                        break
            if (pile[-1] == '$') and (scanner_output[i][0] == '$'):
                print('arvore')
                break
            
        if try_backtrack:
            print('Backtraking...')
            if not pile_backtrack:
                print('Erro na linha ' + str(scanner_output[3]))
                break
            
            try_backtrack = False
            (i, backtracking_aux, pilha_nos, pile) = pile_backtrack.pop()
            pai_errado = pilha_nos.pop()
            tree_nodes = pilha_nos
            tree_nodes.append(Node(pai_errado.name, pai_errado.parent))
            continue
        break
    
    
    tree_file = open('./tree.txt', 'w', encoding="utf-8")
    for pre, _, node in RenderTree(tree):
        tree_file.write("%s%s\n" % (pre, node.name))
    tree_file.close()
            
            

parser(input_4)

