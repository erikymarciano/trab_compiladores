from parser_data import *
from bnf import *
from examples import *

def parser(scanner_output):
    print(scanner_output)
    pile = ['$']
    pile.extend(bnf_rules[0][::-1])
    print(pile)
    error = False
    error_list = []
    
    pile_backtrack:list[(int, int, list[str])] = []
    try_backtrack = False
    backtracking_aux = None
    i = 0
    while(True):
        while pile[-1] != '$' and scanner_output[i] != '$':
            if (pile[-1] == 'ε'):
                pile.pop()
                print(pile)
            else:
                print('Topo da pilha: '+pile[-1])
                print('Token atual: '+scanner_output[i][0]+' posicao('+str(i)+')')
                if (pile[-1] in terminals) and (pile[-1] == scanner_output[i][0]):
                    # match();
                    pile.pop()
                    print(pile)
                    print('acrescentando 1')
                    i = i+1
                else:                    
                    if backtracking_aux:
                        aux = [backtracking_aux]
                        backtracking_aux = None
                    elif pile[-1] in table.keys() and scanner_output[i][0] in table[pile[-1]].keys():
                        aux = table[pile[-1]][scanner_output[i][0]]
                        if len(aux) == 1:
                            # producao()
                            pile.pop()
                            pile.extend(bnf_rules[aux[0]-1][::-1])
                            print(pile)
                        elif len(aux) > 1 and try_backtrack == False:
                            print('entrei elif')
                            for k in range(1, len(aux)):
                                pile_backtrack.append((i, aux[0]-1, pile.copy()))
                            try_backtrack = True
                            break
                        else:
                            print('entrei else')
                            break
                    #INICIO BLOCO TRATAMENTO DE ERROS
                    elif pile[-1] in table.keys() and scanner_output[i][0] not in table[pile[-1]].keys(): 
                        error = True
                        error_list.append('Erro de celula nao preenchida na linha ' + str(scanner_output[i][2]))
                        if scanner_output[i][0] == '$' or (scanner_output[i][0] in follow[pile[-1]]):                            
                            pile.pop()   
                        else:
                            while (scanner_output[i][0] != '$') and ((scanner_output[i][0] not in first[pile[-1]]) and (scanner_output[i][0] not in follow[pile[-1]])):
                                print('acrescentando 1 tratamento de erro')
                                i = i+1
                    #FIM BLOCO TRATAMENTO DE ERROS
                    else:
                        error = True
                        error_list.append('Erro critico na linha ' + str(scanner_output[i][2]) + ' abortando..')
                        print(error_list)
                        return


        if try_backtrack == True:
            
            if not pile_backtrack:
                error = True
                error_list.append('Erro de celula nao preenchida na linha ' + str(scanner_output[i][2]))
                if scanner_output[i][0] == '$' or scanner_output[i][0] in follow[pile[-1]].keys():
                    pile.pop()
                else:
                    while (scanner_output[i][0] != '$') and ((scanner_output[i][0] not in first[pile[-1]]) and (scanner_output[i][0] not in follow[pile[-1]])):
                        print('acrescentando 1 bt')
                        i = i+1                
                continue

            try_backtrack = False
            (i, backtracking_aux, pile) = pile_backtrack.pop()
            continue
        
        if (pile[-1] == '$') and (scanner_output[i][0] == '$'):
            if error == False:
                print('arvore')
                return
            else:
                print(error_list)
                return

        else:
            error_list.append('Erro critico na linha ' + scanner_output[i][2] + ' abortando..')
            print(error_list)
            return         

parser(input_4)