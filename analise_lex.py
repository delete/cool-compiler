# coding: utf-8
import sys

import ply.lex as lex

import tokrules


class MyLex(object):

    def __init__(self, module=tokrules, string=None):
        self.module = module
        self.lexer = None
        self.llex = []

        self._build_lexer()

    def _build_lexer(self):
        self.lexer = lex.lex(module=self.module)

    def tokenize(self, newString=None):
        if newString:
            self.lexer.input(str(newString))

        while 1:
            tok = self.lexer.token()
            if not tok:
                break

            lt = (tok.type, tok.value, tok.lineno, tok.lexpos)
            self.llex.append(lt)

        return tuple(self.llex), tuple(tokrules.lerror)

    # Compute column.
    # input is the input text string
    # token is a token instance
    def find_column(input, token):
        last_cr = input.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column


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
    l = MyLex()
    llex, lerror = l.tokenize(codigo)

    for l in llex:
        print(l)

    print('ERROR')
    for e in lerror:
        print(e)
