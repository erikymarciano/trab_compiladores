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


def parser(scanner_output):
    parser_error_messages = []
    pile = ['$']
    derivacao = bnf_rules[0][::-1]
    pile.extend(derivacao)
    print(pile)
    
    pile_backtrack:list[(int, int, list[Node], list[str], list[str])] = [] # i_entrada, id_regra, estado_lista_nos, estado_da_pilha, lista_de_erros
    try_backtrack = False
    backtracking_aux = None
    i = 0
    tree = Node("<Function>")
    tree_nodes = []
    parser_in_error = False
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
                    parser_in_error = False
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
                            pile_backtrack.append((i, aux[k], tree_nodes.copy(), pile.copy(), parser_error_messages.copy()))
                    if (pile[-1] not in terminals) and (aux != None):
                        # producao()
                        parser_in_error = False
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
                if not parser_in_error:
                    parser_error_messages.append('Erro na linha: {}, token {}'.format(scanner_output[i][2], scanner_output[i][1]))
                parser_in_error = True
                
                if not pile or i >= len(scanner_output):
                    break
            
                if pile[-1] in table.keys() and scanner_output[i][0] not in table[pile[-1]].keys():
                    if scanner_output[i][0] == '$' or (scanner_output[i][0] in follow[pile[-1]]):                            
                        pile.pop()   
                        continue
                elif pile[-1] not in terminals:
                    while (scanner_output[i][0] != '$') and ((scanner_output[i][0] not in first[pile[-1]]) and (scanner_output[i][0] not in follow[pile[-1]])):
                        i = i+1
                else:
                    i = i + 1
                    if i >= len(scanner_output):
                        break
                continue
                
            
            print('Backtraking...')
            
            try_backtrack = False
            (i, backtracking_aux, pilha_nos, pile, parser_error_messages) = pile_backtrack.pop()
            # print((i, backtracking_aux, pilha_nos, pile))
            parser_in_error = False
            tree_nodes = pilha_nos
            pai_errado = pilha_nos[-1]
            pai_errado.children = []
            continue
    
        
        if (pile[-1] != '$' or scanner_output[i][0] != '$') and not parser_in_error:
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

