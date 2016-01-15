# Reserved words
reserved = {
   'class': 'CLASS',
   'else': 'ELSE',
   'if': 'IF',
   'fi': 'FI',
   'in': 'IN',
   'isvoid': 'ISVOID',
   'let': 'LET',
   'loop': 'LOOP',
   'pool': 'POOL',
   'then': 'THEN',
   'while': 'WHILE',
   'case': 'CASE',
   'esac': 'ESAC',
   'new': 'NEW',
   'of': 'OF',
   'not': 'NOT',
   'inherits': 'INHERITS',
   'false': 'FALSE',
   'true': 'TRUE',
}

tokens = [
    'ID', 'REAL', 'INT',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE', 'DELIMITER',
    'AT', 'EQUALS', 'TYPE', 'STRING', 'VAZIO', 'GREATER_THAN',
    'LESS_THAN', 'GTE', 'LTE', 'PRECEDENCE', 'COMMA', 'INT_COMPLEMENT'
] + list(reserved.values())

# Regex dos Tokens
t_EQUALS = r'\='
t_AT = r'<-'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DELIMITER = r'\;'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_TYPE = r'\:'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_GREATER_THAN = r'<'
t_LESS_THAN = r'>'
t_GTE = r'>='
t_LTE = r'>='
t_COMMA = r','
t_ignore = ' \t|\r'
t_INT_COMPLEMENT = r'~'
t_PRECEDENCE = r'@ | ~ | not | isvoid'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_COMMENT(t):
    r'--.* | \(\*([^*]|[\r\n]|(\*+(^|[\r\n])))*\*\)'
    pass


def t_STRING(t):
    r'\".*\n*\s*.*\"'
    # Tira as aspas
    t.value = t.value[1:-1].decode("string-escape")
    return t


def t_REAL(t):
    r'[0-9]+([.,][0-9]+)+'
    try:
        t.value = t.value
    except ValueError:
        print("REAL value too large %d", t.value)
        t.value = 0
    return t


def t_INT(t):
    r'[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_EMPTY(t):
    r'^\n|^\s+|^\t|^\f|^\v|^\r'
    pass


def t_DOT(t):
    r'\.'


lerror = []


def t_error(t):
    lr = (t.value[0], t.lineno, t.lexpos)
    lerror.append(lr)
    t.lexer.skip(1)
