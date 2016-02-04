from collections import defaultdict

from ast import *
from myexceptions import SemantError


class Semant(object):
    """docstring for Semant"""

    def __init__(self, ast):
        self.ast = ast
        self.classes = {}
        self.parents = defaultdict(set)

    def build(self):
        self.__create_default_classes()
        self.__create_inheritance()
        self.__check_undefined_classes()
        self.__check_inheritance_cycles()

    def __create_default_classes(self):
        # Object there is no parent
        objc = Class("Object", None, [
            Method('abort', [], 'Object', None),
            Method('type_name', [], 'String', None),
            Method('copy', [], 'SELF_TYPE', None),
        ])
        # IO inherits from Object
        ioc = Class("IO", "Object", [
            Method('out_string', [('arg', 'String')], 'SELF_TYPE', None),
            Method('out_int', [('arg', 'Int')], 'SELF_TYPE', None),
            Method('in_string', [], 'String', None),
            Method('in_int', [], 'Int', None),
        ])
        stringc = Class("String", "Object", [
            Method('length', [], 'Int', None),
            Method('concat', [('arg', 'String')], 'String', None),
            Method(
                'substr', [('arg1', 'Int'), ('arg2', 'Int')], 'String', None
            ),
        ])

        self.ast += [objc, ioc, stringc]

    def __create_inheritance(self):
        '''
            Create two structures:
            One with all the classes and another with all
            parents classes.
        '''
        for _class in self.ast:
            if _class.name in self.classes:
                raise SemantError('Class %s already defined!' % _class.name)
            else:
                self.classes[_class.name] = _class

            if _class.name != 'Object':
                self.parents[_class.parent].add(_class.name)

    def __check_undefined_classes(self):
        parents = self.parents.keys()
        for parent in parents:

            if parent not in self.classes:
                class_name = self.parents[parent]
                message = 'Classe %s inherit from an undefined parent %s'

                raise SemantError(
                    message % (class_name, parent)
                )

    def __check_inheritance_cycles(self):
        '''
            First, set every class(including parents) as False.
            Then, visit each class and their childs.
        '''
        visited = {}
        for parent_name in self.parents.keys():
            visited[parent_name] = False
            for class_name in self.parents[parent_name]:
                visited[class_name] = False

        print('\n\n====== VISITED BEFORE ======\n\n')
        print(visited)

        self.__visit_tree('Object', visited)

        print('\n\n====== VISITED AFTER ======\n\n')
        print(visited)

        # If some class has False value, means that the visitor
        # couldn't get in that class. So, some class is missing.
        for key, value in visited.items():
            if not value:
                raise SemantError('%s is in a inheritance cycle' % key)

    def __visit_tree(self, _class, visited):
        visited[_class] = True
        print('\nClass: %s\n' % _class)
        print('\nVisited status: %s\n' % visited)

        # If a _class is not in parents,
        # it is not a parent, so, don't have childs. Get out.
        if _class not in self.parents.keys():
            print('%s is not a parent!' % _class)
            return

        for child in self.parents[_class]:
            self.__visit_tree(child, visited)


def semant(ast):
    s = Semant(ast)
    s.build()
    print('\n\n====== CLASSES ======\n\n')
    print(s.classes)
    print('\n\n====== PARENTS ======\n\n')
    print(s.parents)
