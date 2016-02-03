import sys

from src.analise_sint import syntactic
from src.analise_sem import semant


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Choose a cool file to read.')
        sys.exit(1)

    with open(sys.argv[1]) as file:
        code = file.read()

    ast = syntactic(code)
    if ast is None:
        print("Cannot parse!")
        sys.exit(1)

    parents = semant(ast[0])
    print('\nAST\n\n')
    print(ast[0])
    print('\nPARENTS\n\n')
    print(parents)
