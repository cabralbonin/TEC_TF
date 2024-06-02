''' 
    Nome: Claudinei Cabral Junior
    Trabalho TEC - Tradutor de MT Sipser para MT DI e vice-versa.
    
    Para fazer a conversão, o arquivo de entrada deve estar
    em formato .in e no mesmo diretório do arquivo parser_tm.py. 
    
    O arquivo de entrada não deve conter espaços, linhas em branco e comentários.
    
    Para selecionar o arquivo a ser convertido basta inserir o nome
    do arquivo na função convert_tm().
''' 
        
def sipser_to_standard(transitions):
    
    states = set()
    new_transitions = set()
    initial_state = 'initial_state'
    
    new_transitions.add('0 * * l 0')
    new_transitions.add('0 _ # r initial_state') # Marcamos o início da fita
    
    for transition in transitions:
        current_state, current_symbol, new_symbol, direction, new_state = transition.split()
        
        if current_state == '0':
            current_state = initial_state
        if new_state == '0':
            new_state = initial_state
            
        states.add(current_state)
        states.add(new_state)
        
        new_transitions.add(f'{current_state} {current_symbol} {new_symbol} {direction} {new_state}')
    
    for state in states:
        # Para todo estado, se chegamos no inicio da fita, vamos para a direita
        new_transitions.add(f'{state} # * r {state}')
    
    return new_transitions

def standard_to_sipser(transitions):
    
    states = set()
    symbols = set()
    new_transitions = set()
    initial_state = 'initial_state'
    
    new_transitions.add('0 0 # r rewrite_0')  # Estado auxiliar para empurrar para a direita 0 e rescrever depois
    new_transitions.add('0 1 # r rewrite_1')  # Estado auxiliar para empurrar para a direita 1 e rescrever depois
    new_transitions.add('rewrite_0 0 0 r rewrite_0')  # Estado auxiliar para empurrar para a direita 0 e rescrever 0 no lugar
    new_transitions.add('rewrite_0 1 0 r rewrite_1')  # Estado auxiliar para empurrar para a direita 1 e rescrever 0 no lugar
    new_transitions.add('rewrite_0 _ 0 r end_tape')  # Estado auxiliar para empurrar para a direita _ e rescrever 0 no lugar
    new_transitions.add('rewrite_1 1 1 r rewrite_1')  # Estado auxiliar para empurrar para a direita 1 e rescrever 1 no lugar
    new_transitions.add('rewrite_1 0 1 r rewrite_0')  # Estado auxiliar para empurrar para a direita 0 e rescrever 1 no lugar
    new_transitions.add('rewrite_1 _ 1 r end_tape')  # Estado auxiliar para empurrar para a direita _ e rescrever 1 no lugar
    new_transitions.add('end_tape _ + l end_tape')  # Estado auxiliar para marcar final da fita
    new_transitions.add('end_tape * * l end_tape')  # Estado auxiliar que le qualquer simbolo e anda para a esquerda
    new_transitions.add('end_tape # * r initial_state')  # Estado que indica que chegou no inicio da fita novamente e retorna para o inicio da cabeça
    
    
    for transition in transitions:
        current_state, current_symbol, new_symbol, direction, new_state = transition.split()
        
        if current_state == '0':
            current_state = initial_state
        if new_state == '0':
            new_state = initial_state
            
        states.add(current_state)
        states.add(new_state)
        symbols.add(current_symbol)
        symbols.add(new_symbol)
            
        if current_symbol == '_'  and direction == 'l':
            # Empurra simbolo de final de fita para direita e escreve um simbolo no lugar
            end_tape_state = 'end_tape_state_' + current_state
            new_transitions.add(f'{current_state} {current_symbol} {new_symbol} {direction} {new_state}')
            new_transitions.add(f'{current_state} + _ r {end_tape_state}')
            new_transitions.add(f'{end_tape_state} _ + l {current_state}')
            
        else:
            new_transitions.add(f'{current_state} {current_symbol} {new_symbol} {direction} {new_state}')
            
    '''
        Adicionamos para todos os estados, transições que ao lerem #(simbolo de inicio de fita) empurra
        tudo para direita. Fazemos isso através de estados auxiliares que reescrevem o simbolo lido anteriormente.
    '''        
    for state in states:
        push_state = 'push_state' + state
        new_transitions.add(f'{state} # # r {push_state}')
        for from_symbol in symbols:
            from_rewrite_state = 'rewrite_state' + state + '_' + from_symbol
            new_transitions.add(f'{push_state} {from_symbol} _ r {from_rewrite_state}')
            for to_symbol in symbols:
                to_rewrite_state = 'rewrite_state' + state + '_' + to_symbol
                end_tape_state = 'end_state_' + state + '_+'
                goto_begin_state = 'goto_begin_state_' + state
                new_transitions.add(f'{from_rewrite_state} {to_symbol} {from_symbol} r {to_rewrite_state}')
                new_transitions.add(f'{from_rewrite_state} + {from_symbol} r {end_tape_state}')
                new_transitions.add(f'{end_tape_state} _ + l {goto_begin_state}')
                new_transitions.add(f'{goto_begin_state} * * l {goto_begin_state}')
                new_transitions.add(f'{goto_begin_state} # # r {state}')

    return new_transitions


def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        
    type = lines[0].strip()
    transitions = set() 
    
    for line in lines[1:]:
        transitions.add(line) 
        
    return type, transitions


def convert_tm(filename):
    type, transitions = read_file(filename)
    
    if type == ";S":
        print("Convertendo de Sipser para Duplamente Infinita...")
        converted_transitions = sipser_to_standard(transitions)
        output_type = ";I"
    else:
        print("Convertendo de Duplamente Infinita para Sipser...")
        converted_transitions = standard_to_sipser(transitions)
        output_type = ";S"
    
    output_path = filename.replace('.in', '.out')
    with open(output_path, 'w') as f:
        f.write(f"{output_type}\n")
        for transition in converted_transitions:
            f.write(f"{transition}\n")
    
    print(f"Conversão concluida: {output_path}")
        

convert_tm('odd.in')
convert_tm('sameamount10.in')
# convert_tm('palindrome.in')
# convert_tm('prime.in')
# convert_tm('binarytodecimal.in')
# convert_tm('test.in')
