# coding: utf-8
import ply.lex as lex

import sys


def tokenize(codigo):
    # Paralvras reservadas
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
        'LESS_THAN', 'PRECEDENCE', 'COMMA'
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
    t_COMMA = ','

    t_ignore = " \t|\r"

    def t_PRECEDENCE(t):
        r'@ | ~ | not | isvoid'
        return t

    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')    # Check for reserved words
        return t

    def t_COMMENT(t):
        r'--.* | \(\*([^*]|[\r\n]|(\*+(^|[\r\n])))*\*\)'
        pass

    def t_STRING(t):
        r'\".+\n*\s*.+\"'
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

    # Compute column.
    # input is the input text string
    # token is a token instance
    def find_column(input, token):
        last_cr = input.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    lerror = []

    def t_error(t):
        lr = (t.value[0], t.lineno, t.lexpos)
        lerror.append(lr)
        t.lexer.skip(1)

    lexer = lex.lex()

    lexer.input(str(codigo))

    llex = []
    while 1:
        tok = lex.token()
        if not tok:
            break

        lt = (tok.type, tok.value, tok.lineno, tok.lexpos)
        llex.append(lt)

    return (tuple(llex), tuple(lerror))


if __name__ == '__main__':
    codigo = '''class Main inherits IO {
        main() : Object {
        out_string("Hello, world.\n")
        -- comentario
        a : Int;
        a <- 5;
        out_int(2=2)
        };
        };
    '''

    with open(sys.argv[1]) as file:
        codigo = file.read()
    llex, lerror = tokenize(codigo)

    for l in llex:
        print l

    print 'ERROR'
    for e in lerror:
        print e
