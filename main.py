#  Proyecto de automatas
#  Universidad del Valle de Guatemala
#  Teoria de la computacion

#  Autores:
# - Alejandra Guzman 20262
# - Pablo Escobar 20936
# - Jorge Caballeros 20009

from Algorithms import Thompson, subsetConstruction
from directito import DFA
from utils import SyntaxTree





# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
# basado en el algoritmo de Shunting-yard 
def parseRegexToPostfix(regex):
    outputQueue = []
    operatorStack = []
    operatorPrecedence = {
        '*': 3,
        '?': 2,
        '|': 1,
        '+': 1,
        '(': 0,
        ')': 0
    }

    for char in regex:
        if char == '(':
            operatorStack.append(char)
        elif char == ')':
            while operatorStack[-1] != '(':
                outputQueue.append(operatorStack.pop())
            operatorStack.pop()
        elif char in operatorPrecedence:
            while operatorStack and operatorPrecedence[char] <= operatorPrecedence[operatorStack[-1]]:
                outputQueue.append(operatorStack.pop())
            operatorStack.append(char)
        else:
            outputQueue.append(char)

    while operatorStack:
        outputQueue.append(operatorStack.pop())

    return outputQueue
       

# Funcion para revisar que los parentesis esten balanceados
# param - cadena de caracteres
def revisarParentesis(cadena):
    count= 0  
    ans=False  
    for i in cadena:  
        if i == "(":  
            count += 1  
        elif i == ")":  
            count-= 1  
        if count < 0:  
            return ans  
    if count==0:  
        return not ans  
    return ans  

# Funcion para valida que la expresion regular es valida
# param - expresion regular 
def validarExpresionRegular(expresion):
    bandera = False
    caracteres = ["(", ")", "|", "*", "?","+"]
    for caracter in expresion:
        if caracter.isalnum() or caracter in caracteres:
            bandera = True
    return bandera and revisarParentesis(expresion)

   
# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
def createFixedRegex(regex):
    newRegex = ""
    for i in range(len(regex)):
        if i < len(regex) - 1:
            if (regex[i].isalnum() and regex[i + 1].isalnum()) or (regex[i].isalnum() and regex[i + 1] == "(") or (regex[i] == ")" and regex[i + 1].isalnum()) or (regex[i] == ")" and regex[i + 1] == "(") or (regex[i] == "*" and regex[i + 1].isalnum()) or (regex[i] == "*" and regex[i + 1] == "("):
                newRegex += regex[i]  + "?"
            else:
                newRegex += regex[i]
    newRegex += regex[len(regex) - 1]
    return newRegex


if __name__ == "__main__":
    # expresion = input("Ingrese la expresion regular: ")
    # cadena = input("Ingrese la cadena a evaluar: ")

    # Expresion prueba
    expresion = "(a|b)*abbc"
    #REGEX = '(a|b)*abb'
    
    # expresion = "a"   
    
    #   OPERADORES
    
    OPERATORS = {
        '|': 1,
        '^': 2,
        '*': 3,
        '?': 2,
        '+': 1
    }
    EPSILON = '&'
    

    ## Syntax tree construction
    # generate tree from regex
    tree = SyntaxTree(OPERATORS, expresion)




    # Se implemento metodo directo
    # link: https://www.geeksforgeeks.org/regular-expression-to-dfa/
    hash_tree = SyntaxTree(OPERATORS, expresion + "#", direct=True)

    # se consiguen los nodos
    print(hash_tree.traverse_postorder(hash_tree.root))
    nodes = hash_tree.traverse_postorder(hash_tree.root, full=True)
    direct_dfa = DFA(syntax_tree=hash_tree, direct=True, nodes=nodes)
    direct_dfa.direct()
    direct_dfa.graph_automata(mapping=direct_dfa.state_mapping)
    


    if validarExpresionRegular(expresion):
        expresion = createFixedRegex(expresion)
        expresion = parseRegexToPostfix(expresion)
        # print(expresion)
        nfa = Thompson(expresion)
        nfa.setNameToAllStates()
        print("Tabla de transiciones NFA\n")
        nfa.show()
        # print("\n")
        print("\n")
        print("Tabla de transiciones DFA\n")
        print(subsetConstruction(nfa,expresion))
        
        # # Print NFA dictionary in a readable format
        # for key, value in nfa.items():
        #     print(key, value)
        
 


        
     
        


        



