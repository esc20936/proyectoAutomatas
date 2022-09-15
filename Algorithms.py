# Thompson algorithm for building a NFA from a regular expression in postfix notation
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def show(self):
        self.start.show()
    
class State:
    def __init__(self, transitions=None):
        self.transitions = transitions if transitions else {}
    
    def addTransition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

    # print evertything reachable from this state
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

                
# simbolo de epsilon = &
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

# def Thompson(Regex):
#     nfaStack = []
#     for c in Regex:
#         if c == '?':
#             # Concatenation
#             nfa2 = nfaStack.pop()
#             nfa1 = nfaStack.pop()
#             nfa1.end.edges.append(nfa2.start)
#             # nfa1Edges = nfa1.end.edges
#             # nfa2Edges = nfa2.start.edges
#             # temp = State(edges=nfa1Edges + nfa2Edges)
#             # nfa1.start.edges = [temp]
#             # nfa1.end = temp
#             # nfa2.start = temp

#             # nfa1.end.label = nfa2.start.label
#             nfaStack.append(NFA(nfa1.start, nfa2.end))
#         elif c == '|':
#             # Alternation
#             nfa2 = nfaStack.pop()
#             nfa1 = nfaStack.pop()
#             start = State(edges=[nfa1.start, nfa2.start])
#             end = State()
#             nfa1.end.edges.append(end)
#             nfa2.end.edges.append(end)
#             nfaStack.append(NFA(start, end))
#         elif c == '*':
#             # Kleene star
#             nfa = nfaStack.pop()
#             start = State(edges=[nfa.start])
#             end = State()
#             nfa.end.edges += [nfa.start, end]
#             nfaStack.append(NFA(start, end))
#         else:
#             # Literal
#             end = State()
#             start = State(c, [end])
#             nfaStack.append(NFA(start, end))
    
#     return nfaStack.pop()

# # parse Thomspon's NFA to DFA
# def parseNFAtoDFA(nfa):
#     # get all states from NFA
#     states = []
#     def getStates(state):
#         if state not in states:
#             states.append(state)
#             for edge in state.edges:
#                 getStates(edge)
#     getStates(nfa.start)
#     # get all symbols from NFA
#     symbols = []
#     for state in states:
#         if state.label not in symbols:
#             symbols.append(state.label)

#     print("States: ", states)
#     print("Symbols: ", symbols)

#     namesOfStates = {}
#     count = 0
#     for state in states:
#         name = "q" + str(count)
#         namesOfStates[state] = name
#         count += 1

#     # create DFA
#     dfa = {}
#     def getDFA(state, symbol):
#         if state.label == symbol and len(state.edges) > 0:
#             print(len(state.edges))
#             return namesOfStates[state.edges[0]]
#         else:
#             return None
    
    
#     for state in states:
#         dfa[namesOfStates[state]] = {}
#         for symbol in symbols:
#             dfa[namesOfStates[state]][symbol] = getDFA(state, symbol)
#         count += 1
        
#     # print(namesOfStates)
#     return dfa
    

# # function to remove None transitions from DFA
# def removeNoneTransitions(dfa):
    
    

