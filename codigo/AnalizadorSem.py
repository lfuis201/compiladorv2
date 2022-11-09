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
        insertST(variable_fun, "Funcion", gbl_nombre_function)

    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]

            if primer_hijo.symbol.symbol == 'TYPE':
                hermano = primer_hijo.father.children[1]
                variable = hermano.children[0]
                #print("Aqui se crea una variable", variable.lexeme)
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
            print("Variable encontrada")
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


def findSTT(lexeme):
    for symbol in reversed(symbol_table_array):
        #print("PRINT SYMBOLID: ",symbol.id)
        #print("PRINT LEXEME: ", lexeme)
        if symbol.id.strip() == lexeme:
            #print("IF SYMBOL", symbol.id)
            return symbol.type

def setType(node):
    if node.symbol.symbol == 'STATEMENT':
        if len(node.children) > 0:
            primer_hijo = node.children[0]

            if primer_hijo.symbol.symbol == 'TYPE':
                node_tp = primer_hijo.children[0]
                primer_hijo.father.children[1].children[0].type = node_tp.lexeme
            

    for child in node.children:
        setType(child)
        if(child.type != None):
            print("variable de tipo: ",child.type, "en linea: ",child.line)

      


file_name = "test/test1.txt"

# lexer
tokens = get_tokens(file_name)
tokens.append([ '$', None, None ])

root, node_list = parser(tokens)

findVal(root)
print_tree(root, node_list)
setType(root)

