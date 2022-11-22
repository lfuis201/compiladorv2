from AnalizadorLex import get_tokens
from Ll1 import parser, print_tree



class symbolTable:
    def __init__(self, id, typ, category, father = 'main', line = None):
        self.id = id
        self.type = typ
        self.category = category
        self.line = line
        self.father = father

symbol_table_array = []

gbl_nombre_function = 'main'

def insertST(node_var, category, father):
    symbol = symbolTable(node_var.lexeme, node_var.type, category, father, node_var.line)
    symbol_table_array.append(symbol)

def removeST():
    global symbol_table_array
    symbol_table_temp = []
    for symbol in symbol_table_array:
        if symbol.father != gbl_nombre_function:
            symbol_table_temp.append(symbol)
    symbol_table_array = symbol_table_temp

def findST(lexeme):
    val = False
    for symbol in reversed(symbol_table_array):
        #print("SYMBOl: ",symbol.id)
        #print("LEXEMA: ", lexeme)
        if symbol.id.strip() == lexeme:
            val = True
    return val

def printST():
    for i in symbol_table_array:
        print(i.id, i.type, i.category, i.father, i.line)



def findVal(node):
    global gbl_nombre_function
    if node.symbol.symbol == 'FUNCTION':
        tercer_hijo = node.children[2]
        gbl_nombre_function = tercer_hijo.lexeme
        #print(gbl_nombre_function)

        variable_fun = node.children[2]
        if (findST(variable_fun.lexeme)):
            print("Eror funcion ya definida", variable_fun.line)
        else:
            insertST(variable_fun, "func", "BLOCK")
            print("FUNCION creada", variable_fun.line)

    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]
            segudno_hijo = node.children[1]
            
            if primer_hijo.symbol.symbol == 'TYPE':
                hermano = primer_hijo.father.children[1]
                variable = hermano.children[0]
                if (findST(variable.lexeme)):
                    
                    print("ERROR SEMANTICO VARIABLE YA DEFINIDA")
                else:
                #buscar si existe, true error semantico (ya definida)
                #insertar en tabla
                    insertST(variable, "Variable", gbl_nombre_function)
    
    if node.symbol.symbol == 'id':
        #printST()
        #print(node.lexeme)
        #print("uso la variable", node.lexeme)
        #buscar en la tabla, false error semantico (variable no definida)
        if (findST(node.lexeme)):
            print("Variable encontrada", node.line )
        else:
            print("ERROR SEMANTICO VARIABLE NO DEFINIDA", node.lexeme, node.line)
    
    


    if node.symbol.symbol == 'keyr':
        #print("PADRE DE KEYR: ", node.father.symbol.symbol)
        #print("ENTRANDO A KEYR")
        if node.father.father.symbol.symbol == 'FUNCTION_M':
            #print("ENTRANDO A FUNCSTION_M")
            gbl_nombre_function = 'main'
            removeST()
        if node.father.symbol.symbol == 'BLOCK':
            removeST()
            #print("ENTRANDO A BLOCK")

    for child in node.children:
        findVal(child)


#buscar por tipo
def findSTT(lexeme):
    for symbol in reversed(symbol_table_array):
        #print("PRINT SYMBOLID: ",symbol.id)
        #print("PRINT LEXEME: ", lexeme)
        if symbol.id.strip() == lexeme:
            #print("IF SYMBOL", symbol.id)
            return symbol.type
#setear tipos
def setType(node):
    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]
            segundo_hijo = node.children[1]

            if primer_hijo.symbol.symbol == 'TYPE':
                node_tp = primer_hijo.children[0]
                primer_hijo.father.children[1].children[0].type = node_tp.lexeme

    for child in node.children:
        setType(child)
        if child.type != None:
           print("variable de tipo: ",child.type, "en linea: ",child.line)

#recorrer nodo STATEMENT con nodo E
def setTypeE(node):
    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]
            if primer_hijo.symbol.symbol == 'id':
                
                lex = findSTT(primer_hijo.lexeme)
                if lex:
                    primer_hijo.type = lex

        if len(node.children) > 2:
            
            tercer_hijo = node.children[2]
            if tercer_hijo.symbol.symbol == 'E':
                setTypeT(tercer_hijo)

    for child in node.children:
        setTypeE(child)

#recorre nodo T
def setTypeT(node):
    node_E = node
    node.type = 'int'
    if node_E.children[0].symbol.symbol == 'T':
        node_TERM = node_E.children[0].children[0]
        if node_TERM.symbol.symbol == 'TERM':
            if node_TERM.children[0].symbol.symbol == 'num':
                node_TERM.children[0].type = 'int'
            elif node_TERM.children[0].symbol.symbol == 'id':
                lex = findSTT(node_TERM.children[0].lexeme)
                #print("IMPRIMIENDO LEX ", lex)
                if lex:
                    node_TERM.children[0].type = lex
            elif node_TERM.children[0].symbol.symbol == 'boolean':
                node_TERM.children[0].type = 'bool'
        else:
            print("error de tipos a", node_TERM.children[0].line)
    if node_E.children[1].symbol.symbol == 'E\'':
        setTypeEprim(node_E.children[1])
        

#Recorrer nodo E'
def setTypeEprim(node):
    node_Ee = node
    if len(node_Ee.children) > 1:
        node_TERM = node_Ee.children[1].children[0]
        node_OPE = node_Ee.children[0].children[0]
        if node_TERM.symbol.symbol == 'TERM' and node_OPE == "OPER":
            if node_TERM.children[0].symbol.symbol == 'num':
                node_TERM.children[0].type = 'int'
                
            elif node_TERM.children[0].symbol.symbol == 'id':
                lex = findSTT(node_TERM.children[0].lexeme)
                
                if lex:
                    node_TERM.children[0].type = lex
                    
            elif node_TERM.children[0].symbol.symbol == 'boolean':
                node_TERM.children[0].type = 'bool'
                
        
        else:
            print("error de tipos", node_TERM.children[0].line)
        
        

def printroot(node):
    for child in node.children:
        print(str(node.symbol.symbol) + ' -> ' + str(child.symbol.symbol) + '; \n')
        printroot(child)
     
file_name = "test/test1.txt"

# lexer
tokens = get_tokens(file_name)
tokens.append([ '$', None, None ])

root, node_list = parser(tokens)

setType(root)
findVal(root)

print_tree(root, node_list)
#printroot(root)