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
        self.create_default_classes()
        self.create_inheritance()

    def create_default_classes(self):
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

    def create_inheritance(self):
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


def semant(ast):
    s = Semant(ast)
    s.build()
    print('\n\nCLASSES\n\n')
    print(s.classes)
    return s.parents
