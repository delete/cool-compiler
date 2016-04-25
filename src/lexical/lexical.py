# coding: utf-8
import sys

import ply.lex as lex

from commom import find_column
import tokrules


class MyLex(object):

    def __init__(self, module=tokrules):
        self.module = module
        self.lexer = None
        self.llex = []

        self._build_lexer()

    def _build_lexer(self):
        self.lexer = lex.lex(module=self.module)

    def tokenize(self, newString):
        self.lexer.input(str(newString))

        while True:
            tok = self.lexer.token()
            if not tok:
                break
            lt = (tok.type, tok.value, tok.lineno, find_column(newString, tok))
            self.llex.append(lt)

        return tuple(self.llex), tuple(tokrules.lerror)


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
    if len(sys.argv) != 2:
        print('Choose a cool file to read.')
        sys.exit(1)

    with open(sys.argv[1]) as file:
        codigo = file.read()
    l = MyLex()
    llex, lerror = l.tokenize(codigo)

    for l in llex:
        print(l)

    print('ERROR')
    for e in lerror:
        print(e)
