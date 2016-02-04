import sys

from src import syntactic
from src import semant
from src import lex


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

    semant(ast[0])
    print('\n\n====== AST ======\n\n')
    print(ast[0])
