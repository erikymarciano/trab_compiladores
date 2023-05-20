from anytree import Node, RenderTree
from parser_data import *
from bnf import *
from examples import *

output_test = open('./scanner_output.txt')
saida = output_test.read().split('\n')
formatted_output = []
for element in saida:
    formatted_output.append(eval(element))
output_test.close()

parser_error_messages = []

def parser(scanner_output):
    pile = ['$']
    derivacao = bnf_rules[0][::-1]
    pile.extend(derivacao)
    print(pile)
    
    pile_backtrack:list[(int, int, list[Node], list[str])] = [] # i_entrada, id_regra, estado_lista_nos, estado_da_pilha
    try_backtrack = False
    backtracking_aux = None
    i = 0
    tree = Node("<Function>")
    tree_nodes = []
    for item in derivacao:
        node = Node(item, parent=tree)
        tree_nodes.append(node)
    while(True):
        while pile[-1] != '$' and scanner_output[i][0] != '$':
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
                            pile_backtrack.append((i, aux[0]-1, tree_nodes.copy(), pile.copy()))
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
            
        if try_backtrack:
            if not pile_backtrack:
                parser_error_messages.append('Erro na linha: {}, token {}'.format(scanner_output[i][2], scanner_output[i][1]))
                
                if pile[-1] in table.keys() and scanner_output[i][0] not in table[pile[-1]].keys():
                    if scanner_output[i][0] == '$' or (scanner_output[i][0] in follow[pile[-1]]):                            
                        pile.pop()   
                    else:
                        while (scanner_output[i][0] != '$') and ((scanner_output[i][0] not in first[pile[-1]]) and (scanner_output[i][0] not in follow[pile[-1]])):
                            i = i+1
                    continue
                
                break
            
            print('Backtraking...')
            try_backtrack = False
            (i, backtracking_aux, pilha_nos, pile) = pile_backtrack.pop()
            print((i, backtracking_aux, pilha_nos, pile))
            tree_nodes = pilha_nos
            pai_errado = pilha_nos[-1]
            pai_errado.children = []
            continue
    
        
        if pile[-1] != '$' or scanner_output[i][0] != '$':
            parser_error_messages.append('Erro na linha: {}, token {}'.format(scanner_output[i][2], scanner_output[i][1]))

        break
    
    
    tree_file = open('./parser_output.txt', 'w', encoding="utf-8")
    if not parser_error_messages:
        for pre, _, node in RenderTree(tree):
            tree_file.write("%s%s\n" % (pre, node.name))
    else:
        print("[Parser Error]")
        tree_file.write('\n'.join(parser_error_messages))
    tree_file.close()
    
            
    

parser(formatted_output)

