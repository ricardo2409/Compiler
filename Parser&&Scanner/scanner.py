import ply.lex as lex

# Lista de tokens
tokens = ['ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', #Operators
          'ASSIGN', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', # Operators
          'GREATEROREQUAL', 'LESSOREQUAL', 'AND', 'OR', 'NOT', # Operators
          'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', # Delimiters
          'COMMA', 'SEMICOLON', # Delimiters
          'INT', 'STRING', 'FLOAT', 'BOOLEAN', 
]

# Diccionario de palabras reservadas
reserved = {
    'main': 'MAIN',
    'if':'IF',
    'else':'ELSE',
    'while':'WHILE',
    'print': 'PRINT',
    'function': 'FUNCTION',
    'return' : 'RETURN',
    'true': 'TRUE',
    'false': 'FALSE',
    'program': 'PROGRAM',
    'int': 'INTTYPE',
    'bool': 'BOOLTYPE',
    'float': 'FLOATTYPE',
    'string': 'STRINGTYPE',
    'void': 'VOID',
    'input': 'INPUT', 
    'var': 'VAR',
    'drawbarchart' : 'DRAWBARCHART',
    'drawdotchart' : 'DRAWDOTCHART',
    'drawlinechart' : 'DRAWLINECHART',
    'drawhistchart' : 'DRAWHISTCHART',
    'drawpolychart' : 'DRAWPOLYCHART'
    
}

tokens = tokens+list(reserved.values())

# Caracteres ignorados

t_ignore = ' \t\r'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'\='
t_EQUAL = r'\=='
t_NOTEQUAL = r'\!='
t_GREATER = r'\>'
t_LESS = r'\<'
t_GREATEROREQUAL = r'>='
t_LESSOREQUAL = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'\!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_STRING = r'\".*\" | \'.*\''

# Definicion del ID token
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Revisar si hay palabras reservadas
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

# Definicion de regla para poder llevar el numero de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass
    # Sin valor de retorno, se descarta token

# Regla para manejo de errores
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()


