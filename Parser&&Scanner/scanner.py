import ply.lex as lex

# List of tokens
tokens = ['ID', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', #Operators
          'ASSIGN', 'EQUAL', 'NOTEQUAL', 'GREATER', 'LESS', # Operators
          'GREATEROREQUAL', 'LESSOREQUAL', 'AND', 'OR', 'NOT', # Operators
          'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', # Delimiters
          'COMMA', 'SEMICOLON', # Delimiters
          'INT', 'STRING', 'FLOAT', 'BOOLEAN', 
]

# Dictionary of reserved words
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
    'input': 'INPUT', #Checar**************
    'var': 'VAR',
    'drawbarchart' : 'DRAWBARCHART',
    'drawdotchart' : 'DRAWDOTCHART'
    
}

tokens = tokens+list(reserved.values())

# Ignored characters

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

# ID token definition
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


'''
f = open(filename,"r")

# Give the lexer some input
lexer.input(f.read())

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)

print("\n")
return tokens
'''