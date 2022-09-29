
"""
llorar en automata 

Clase de algoritmo directo

Clase de teoría de la compu

videos de apoyo: 
    https://www.youtube.com/watch?v=I57LsyTdop8
    https://www.youtube.com/watch?v=G8i_2CUHP_Y&t=1082s
"""

import os
from timeit import default_timer as timer
from datetime import timedelta
import uuid
import shortuuid
import graphviz, tempfile

from utils import Stack, Colors



shortuuid.set_alphabet("0123456789")


class FA(object):
    """
        instancia un automata finito
    """
    def __init__(self, symbols, states, tfunc, istate, tstate):
        self.states = states
        self.symbols = symbols
        self.transition_function = tfunc
        self.initial_state = istate
        self.terminal_states = tstate
        
    def setNombre(self, name):
        self.name = name
        
    
    def print_automata(self, type, i_state, t_state, states, symbols, t_function, state_mapping=None):
        print(Colors.OKBLUE  + Colors.ENDC  + Colors.UNDERLINE + type + Colors.ENDC + " AUTOMATA")
        print(Colors.OKCYAN + " Estado inicial " + Colors.ENDC)
        print(" :)", i_state)
        print(Colors.OKCYAN + " Estado terminal" + Colors.ENDC)
        print(" :)", t_state)
        print(Colors.OKCYAN + " Estados " + Colors.ENDC)
        print(" :)")
        for state in states:
            print("     ", state)
        print(Colors.OKCYAN + " Simbolos" + Colors.ENDC)
        print(" :)", symbols)
        if state_mapping:
            print(Colors.OKCYAN + " Mapa de estados" + Colors.ENDC)
            print(" :)")
            for key, value in state_mapping.items():
                print("     ", key, "***", value)
        print(Colors.OKCYAN + " Transiciones" + Colors.ENDC)
        print(" °")
        for key, value in t_function.items():
            print("     ", key, "***", value)
        print("")
        
        
    def graph_automata(self, mapping=None):
        builder = graphviz.Digraph(graph_attr={'rankdir':'LR'})
        
        for x in self.states:
            x = x if not mapping else mapping[tuple(x)]
            if x not in self.terminal_states:
                builder.attr('node', shape='circle')
                builder.node(x)
            else:
                builder.attr('node', shape='doublecircle')
                builder.node(x)
                
        builder.attr('node', shape='none')
        builder.node('')
        builder.edge('', self.initial_state)
        
        for key, value in self.transition_function.items():
            if isinstance(value, str):
                builder.edge(key[0], value, label=(key[1]))
            else:
                for val in value:
                    builder.edge(key[0], val, label=(key[1]))
        
        builder.view(tempfile.mktemp('.gv'), cleanup=True, )
        
        
    def simulate(self):
        raise Exception ("No es posible generar la simulación")


class DFA(FA):
    def __init__(self, nfa=None, syntax_tree=None, symbols=None, states=[], tfunc={}, istate=None, tstate=[], direct=False, nodes=None):
        self.syntax_tree = syntax_tree
        self.nfa = nfa
        self.nodes = nodes
        self.state_mapping = None
        
        # Elimina la epsilon de los simbolos debido a que afecta la construccion remove 
        nfa and '&' in nfa.symbols and nfa.symbols.remove('&')
        syntax_tree and '&' in syntax_tree.symbols and syntax_tree.symbols.remove('&')
        
        # instanciamos al objeto 
        FA.__init__(
            self, 
            symbols=nfa.symbols if nfa else syntax_tree.symbols,
            states=states, 
            tfunc=tfunc,
            istate=istate, 
            tstate=tstate
        )
        
    
    def follow_pos(self):
        self.followpos = {}
        
        for node in self.nodes:
            if node.pos:
                self.followpos[node.pos] = []
            
        for node in self.nodes:
            if node.data == '^':
                for i in node.left.lastpos:
                    self.followpos[i] += node.right.firstpos
                    
            if node.data == '*':
                for i in node.lastpos:
                    self.followpos[i] += node.firstpos
    
    
    def direct(self):
        self.follow_pos()

        
        print(self.followpos)
        
        final_pos = 0
        
        for node in self.nodes:
            if node.data == '#':
                final_pos = node.pos

        t_func = {}
        subset_mapping = {}
        
        dstates_u = [self.syntax_tree.root.firstpos]
        dstates_m = []
        
        while len(dstates_u) > 0:
            T = dstates_u.pop(0)
            dstates_m.append(T)
            
            for symbol in self.symbols:
                U = []
                for node in self.nodes:
                    if node.data == symbol and node.pos in T:
                        U += self.followpos[node.pos]
                        U = list(set(U))
                
                if len(U) > 0:
                    if U not in dstates_u and U not in dstates_m:
                        dstates_u.append(U)
                        
                    try: 
                        subset_mapping[tuple(T)]
                    except:
                        subset_mapping[tuple(T)] = shortuuid.encode(uuid.uuid4())[:4]
                        
                    try:
                        subset_mapping[tuple(U)]
                    except:
                        subset_mapping[tuple(U)] = shortuuid.encode(uuid.uuid4())[:4]
                        
                    
                    t_func[(subset_mapping[tuple(T)], symbol)] = subset_mapping[tuple(U)]                        

        for state in dstates_m:
            if final_pos in state:
                self.terminal_states.append(subset_mapping[tuple(state)])

        self.initial_state = subset_mapping[tuple(dstates_m[0])]
        self.states = dstates_m
        self.transition_function = t_func
        self.state_mapping = subset_mapping
        
        self.print_automata("Dfa directo", self.initial_state, self.terminal_states, self.states, self.symbols, self.transition_function, state_mapping=subset_mapping)
    
    
    def subset(self):
        t_func = {}
        subset_mapping = {}
        
        dstates_u = [self.e_closure_state(self.nfa.initial_state, self.nfa.transition_function)]
        dstates_m = []
        
        while len(dstates_u) > 0:
            T = dstates_u.pop(0)
            dstates_m.append(T)
            
            for symbol in self.symbols:
                U = self.e_closure_set(self.move(T, symbol, self.nfa.transition_function), self.nfa.transition_function)
                
                if len(U) > 0:
                    if U not in dstates_u and U not in dstates_m:
                        dstates_u.append(U)
                    
                    try: 
                        subset_mapping[tuple(T)]
                    except:
                        subset_mapping[tuple(T)] = shortuuid.encode(uuid.uuid4())[:4]
                                              
                    try:
                        subset_mapping[tuple(U)]
                    except:
                        subset_mapping[tuple(U)] = shortuuid.encode(uuid.uuid4())[:4]
                        

                    t_func[(subset_mapping[tuple(T)], symbol)] = subset_mapping[tuple(U)]
                    
        
        for states in dstates_m:
            for state in states:
                if state in self.nfa.terminal_states:
                    self.terminal_states.append(subset_mapping[tuple(states)])
                
        self.initial_state = subset_mapping[tuple(dstates_m[0])]
        self.states = dstates_m 
        self.transition_function = t_func
        self.state_mapping = subset_mapping
        
        self.print_automata("DFA", self.initial_state, self.terminal_states, self.states, self.symbols, self.transition_function, state_mapping=subset_mapping)
    
    
    def e_closure_state(self, s, transition_function):
        closure = [s]
        
        stack = Stack()
        stack.push(s)
        
        while not stack.is_empty():
            state = stack.pop()
            
            for key in transition_function.keys():
                if key[0] == state and key[1] == '&':
                    for x in transition_function[key]:
                        if x not in closure:
                            closure.append(x)
                            stack.push(x)
            
            
        return closure
    
    
    def e_closure_set(self, T, transition_function):
        t_func = transition_function
        stack = Stack()
        
        for t in T:
            stack.push(t)
            
        closure = T[:]
        
        while not stack.is_empty():
            top = stack.pop()
            
            for key, value in t_func.items():
                if key[0] == top and key[1] == '&':
                    for x in value:
                        if x not in closure:
                            closure.append(x)
                            stack.push(x)
                    
        return closure            
    
    
    def move(self, sset, symbol, transition_function):
        move_set = []
        
        for key in transition_function.keys():
            if key[0] in sset and key[1] == symbol: 
                for x in transition_function[key]:
                    move_set.append(x)
            
        return move_set
    
    
    def simulate(self, string):
        start = timer()
        
        s = self.initial_state
        terminal = False
        
        for char in string:
            if char not in self.symbols:
                print(Colors.FAIL  + Colors.ENDC + " Símbolo " + char + " no reconocido por el autómata")
                terminal = None
                break
                exit()
            
            try:
                s = self.transition_function[(s, char)]
            except:
                break
        
        terminal = True if s in self.terminal_states else terminal
        
        end = timer()
        
        return ((end - start) * 1000, terminal if terminal is None else "Ejecutado con exito" if terminal else "No es posible ejecutar")