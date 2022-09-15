# Clase que nos ayudara a crear un NFA
# Atributos:
#   start - Estado inicial
#   end - Estado final
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def show(self):
        self.start.show()

    def getAllStates(self):
        return list(self.start.getAllStates())

# Clase que nos ayudara a representar un estado
# Atributos:
#   transitions - Diccionario que contiene las transiciones del estado
class State:
    def __init__(self, transitions=None):
        self.transitions = transitions if transitions else {}
    
    def addTransition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

    def show(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        print(f"{self} =  {self.transitions}")
        for key in self.transitions:
            for state in self.transitions[key]:
                state.show(visited)

    def getAllStates(self, visited=None):
        if visited is None:
            visited = set()
        if self in visited:
            return
        visited.add(self)
        for key in self.transitions:
            for state in self.transitions[key]:
                state.getAllStates(visited)
        return visited
    
       
# simbolo de epsilon = &
# Algoritmo de Thompson para convertir una expresion regular a un NFA
def Thompson(Regex):
    NFAstack = []
    for char in Regex:

        if char == '|':
            nfa2 = NFAstack.pop()
            nfa1 = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa1.start)
            start.addTransition('&', nfa2.start)
            nfa1.end.addTransition('&', end)
            nfa2.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '?':
            nfa2 = NFAstack.pop()
            nfa1 = NFAstack.pop()
            nfa1.end.transitions = {**nfa1.end.transitions,** nfa2.start.transitions}
            NFAstack.append(NFA(nfa1.start, nfa2.end))

        elif char == '*':
            nfa = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa.start)
            start.addTransition('&', end)
            nfa.end.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        elif char == '+':
            nfa = NFAstack.pop()
            start = State()
            end = State()
            start.addTransition('&', nfa.start)
            nfa.end.addTransition('&', nfa.start)
            nfa.end.addTransition('&', end)
            NFAstack.append(NFA(start, end))

        else:
            end = State()
            start = State(transitions={char: [end]})
            NFAstack.append(NFA(start, end))
            
    return NFAstack.pop()

# Function to convert Epislon NFA to NFA
def EpsilonNFAtoNFA(NFA,expression):
    # Get all states
    states = NFA.getAllStates()
    # Get all symbols
    def getSymbols(expression):
        symbols = []
        for char in expression:
            if char not in symbols and char not in ['|', '*', '?', '+', '(', ')']:
                symbols.append(char)
        return symbols

    symbols = getSymbols(expression)
    
    # TODO: Crear NFA de Epsilon-NFA

    # TODO: Crear DFA de NFA




            
               


        

