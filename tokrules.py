# Reserved words
reserved = [
    'class', 'in', 'inherits', 'isvoid', 'let', 'new', 'of', 'not',
    'loop', 'pool', 'case', 'esac', 'if', 'then', 'else', 'fi', 'while'
]

tokens = [
   'COMMENTINLINE', 'DARROW', 'CLASS', 'IN', 'INHERITS', 'ISVOID', 'LET',
   'NEW', 'OF', 'NOT', 'LOOP', 'POOL', 'CASE', 'ESAC', 'IF', 'THEN', 'ELSE',
   'FI', 'WHILE', 'ASSIGN', 'LE', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN',
   'RPAREN', 'LBRACE', 'RBRACE', 'DOT', 'COLON', 'COMMA', 'SEMI', 'EQ',
   'NEG', 'LT', 'AT', 'TYPEID', 'OBJECTID', 'INT_CONST', 'STR_CONST',
   'COMMENT', 'BOOL_CONST'
]

# Regex dos Tokens
t_DARROW = '=>'
t_ASSIGN = '<-'
t_LE = '<='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_COLON = ':'
t_COMMA = ','
t_SEMI = ';'
t_EQ = '='
t_NEG = '~'
t_LT = '<'
t_AT = '@'

t_ignore = ' \t\r\f'


# Handle objects_types_and_reserved_words
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value == 'true':
        t.type = 'BOOL_CONST'
        t.value = True
        return t
    if t.value == 'false':
        t.type = 'BOOL_CONST'
        t.value = False
        return t

    if t.value.lower() in reserved:
        t.type = t.value.upper()
    else:
        if t.value[0].islower():
            t.type = 'OBJECTID'
        else:
            t.type = 'TYPEID'
    return t


def t_COMMENT(t):
    r'--.* | \(\*([^*]|[\r\n]|(\*+(^|[\r\n])))*\*\)'
    pass


def t_STRING(t):
    r'\".*\n*\s*.*\"'
    # Tira as aspas (only python 2)
    t.value = t.value[1:-1].decode("string-escape")
    t.type = 'STR_CONST'
    return t


def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


lerror = []


def t_error(t):
    lr = (t.value[0], t.lineno, t.lexpos)
    lerror.append(lr)
    t.lexer.skip(1)
