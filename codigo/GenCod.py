from AnalizadorLex import get_tokens
from Ll1 import parser
from AnalizadorSem import findVal

file_out = open ("code.s","w")
def genera_assembler(root):
    file_out.write(".data\n")
    crea_variable(root)#escribe cada variable
    file_out.write(".text\nmain:\n")
    file_out.write("\n \tli $v0,10 \n \tsyscall ")
    
def crea_variable (node):
    #if len(node.children) > 0:
    if node.symbol.symbol == 'TYPE':
        if node.father.symbol.symbol == 'STATEMENT':
            #print("ESTO ESTA IMPRIMIENDO", node.father.children[1].children[0].symbol.symbol)
            #print(len(node.children))
            expre = node.father.children[1].children[2]
            term = expre.children[0].children[0]
            val = term.children[0]
            file_out.write("\tvar_" + str(node.father.children[1].children[0].lexeme) + ": .word 0:1"+"\n")
    for child in node.children:
        crea_variable(child)
def hacersuma(node):
    #if len(node.children) > 0:
    if node.symbol.symbol == 'TYPE':
        if node.father.symbol.symbol == 'STATEMENT':
            #print("ESTO ESTA IMPRIMIENDO", node.father.children[1].children[0].symbol.symbol)
            #print(len(node.children))
            expre = node.father.children[1].children[2]
            term = expre.children[0].children[0]
            val = term.children[0]
            
    for child in node.children:
        crea_variable(child)

if __name__ == "__main__":
    file_name="test/test1.txt"

    #lexer
    tokens = get_tokens (file_name)
    tokens.append (['$', None, None])
    
    #analizador sintatico
    root, node_list = parser(tokens)
    #analizador semantico
    #buscar_if_else(root)
    findVal(root)#check_nodes(root)
    #set_types(root)
    #code generation
    genera_assembler(root)

    file_out.close()