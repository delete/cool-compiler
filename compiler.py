import sys

from src import syntactic
from src import Semant
from src import lex

DEBUG = False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Choose a cool file to read.')
        sys.exit(1)

    with open(sys.argv[1]) as file:
        code = file.read()

    l = lex()
    llex, lerror = l.tokenize(code)
    if lerror:
        print('Lex - EROOR')
        print(lerror)
        sys.exit(1)

    ast = syntactic(code)
    if ast[0] is None:
        print("Sintatic - ERROR")
        sys.exit(1)

    if DEBUG:
        print('\n\n====== DEBUGGING ======\n\n')
    s = Semant(ast[0])
    s.build()

    if DEBUG:
        print('\n\n====== CLASSES ======\n\n')
        print(s.classes)
        print('\n\n====== PARENTS ======\n\n')
        print(s.parents)
        print('\n\n====== AST ======\n\n')
        print(ast[0])
