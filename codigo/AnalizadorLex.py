import ply.lex as lex

reservadas = {
    'main' : 'main',
    'int' : 'int',
    'bool' : 'bool',
    'return' : 'return',
    'function' : 'function',
    'if' : 'if',
    'else' : 'else',
    'while' : 'while',
    'for' : 'for',
    'print' : 'print'
    }



tokens = [
    'num',
    'boolean',
    'opemasmas',
    'opesuma',
    'opemenos',
    'opemult',
    'opediv',
    'opemod',
    'igualq',
    'noigualq',
    'menorq',
    'menoriguq',
    'mayorq',
    'mayoiguq',
    'parenl',
    'parenr',
    'and',
    'or',
    'equal',
    'keyl',
    'keyr',
    'id',
    'comma',
    'dotcomma',
] + list(reservadas.values())


#tokens = tokens+reservadas

t_ignore     = " \t" # Caracteres ignorados
t_opemasmas  = r'\+\+'
t_opesuma    = r'\+'
t_opemenos   = r'\-'
t_opemult    = r'\*'
t_opediv     = r'/'
t_opemod     = r'%'
t_and        = r'&'
t_or         = r'\|'
t_equal     = r'='
t_igualq     = r'=='
t_noigualq   = r'<>'
t_menorq     = r'<'
t_menoriguq   = r'<='
t_mayorq     = r'>'
t_mayoiguq   = r'>='
t_parenl     = r'\('
t_parenr     = r'\)'
t_keyl       = r'\{'
t_keyr       = r'\}'
t_comma      = r'\,'
t_dotcomma   = r'\;'


def t_num(t):
    r'\d+'
    t.value = int(t.value)  # guardamos el valor del lexema  
    return t

def t_boolean(t):
    r'true | false'
    return t

def t_id(t):
    r'[a-zA-Z]+ ( [a-zA-Z0-9]* )'    
    t.type = reservadas.get(t.value,'id')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

#comentarios
def t_COMMENT(t):
    r'\-->.*'

lexer = lex.lex()

def get_tokens(file):
    tokens = []

    f = open(file, "r")
    data = f.read()

    lexer.input(data)
    
    # Tokenize
    while True:
        unitok=[]
        tok = lexer.token()
        if not tok: 
            break
        tokens.append( [tok.type, tok.value, tok.lineno] )

    return tokens

if __name__ == "__main__":
    tokens = get_tokens("test/test1.txt")
    for tok in tokens:
        print( str(tok) + ' ', end='\n')
    print()