# Thompson algorithm for building a NFA from a regular expression in postfix notation
class NFA:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    
class State:
    def __init__(self, label=None, edges=None):
        self.label = label
        self.edges = edges or []
        


def Thompson(Regex):
    nfaStack = []
    for c in Regex:
        if c == '?':
            # Concatenation
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            # nfa1.end.edges.append(nfa2.start)
            nfa1Edges = nfa1.end.edges
            nfa2Edges = nfa2.start.edges
            temp = State(edges=nfa1Edges + nfa2Edges)

            nfa1.end = temp
            nfa2.start = temp

            # nfa1.end.label = nfa2.start.label
            nfaStack.append(NFA(nfa1.start, nfa2.end))
        elif c == '|':
            # Alternation
            nfa2 = nfaStack.pop()
            nfa1 = nfaStack.pop()
            start = State(edges=[nfa1.start, nfa2.start])
            end = State()
            nfa1.end.edges.append(end)
            nfa2.end.edges.append(end)
            nfaStack.append(NFA(start, end))
        elif c == '*':
            # Kleene star
            nfa = nfaStack.pop()
            start = State(edges=[nfa.start])
            end = State()
            nfa.end.edges += [nfa.start, end]
            nfaStack.append(NFA(start, end))
        else:
            # Literal
            end = State()
            start = State(c, [end])
            nfaStack.append(NFA(start, end))
    
    return nfaStack.pop()

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
    
    

