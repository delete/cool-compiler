from collections import defaultdict
from copy import deepcopy

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
        self.__recursive_inheritence()

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

    def __recursive_inheritence(self, _class='Object'):
        '''
            Check attributes and methods from inheritance and
            if it is ok, add them from parent to child.
        '''
        cl = self.classes[_class]

        if cl.parent:
            _class_parent = self.classes[cl.parent]

            attrs_of_parent = self.__get_attributes(_class_parent)
            attrs_of_child = self.__get_attributes(cl)

            self.__check_same_attribute(attrs_of_parent, attrs_of_child)

            methods_of_parent = self.__get_methods(_class_parent)
            methods_of_child = self.__get_methods(cl)

            method_signatures_of_parent = self.__get_signatures(
                                            methods_of_parent
                                        )
            method_signatures_of_child = self.__get_signatures(
                                            methods_of_child
                                        )

            self.__check_same_signature(
                methods_of_child,
                method_signatures_of_parent,
                method_signatures_of_child
            )

            self.__add_method_from_parent_to_child(
                cl, methods_of_parent, methods_of_child
            )

            self.__add_attr_from_parent_to_child(cl, attrs_of_parent)

        # Go recursively
        all_children = self.parents[_class]
        for child in all_children:
            self.__recursive_inheritence(child)

    def __get_attributes(self, _class):
        return [i for i in _class.feature_list if isinstance(i, Attr)]

    def __check_same_attribute(self, parent, child):
        '''
            It's illegal to redefine attribute names in child class.
        '''
        for p_attr in parent:
            for c_attr in child:
                if p_attr.name == c_attr.name:
                    raise SemantError(
                        "Attribute cannot be redefined \
                        in child class %s" % cl.name
                    )

    def __get_methods(self, _class):
        return [i for i in _class.feature_list if isinstance(i, Method)]

    def __get_signatures(self, methods):
        method_signatures = {}
        for method in methods:
            method_signatures[method.name] = {}
            for formal in method.formal_list:
                # formal is a tuple that has 2 values:
                # The first one is the name of the argument;
                # The second, is the type of the argument (Int, Bool,...)
                method_signatures[method.name][formal[0]] = formal[1]
            method_signatures[method.name]['return'] = method.return_type
        return method_signatures

    def __check_same_signature(self, child_methods, sig_parent, sig_child):
        '''
            If a class "B" inherits a method "m" from an ancestor class "A",
            then "B" may override the inherited definition of "m" provided
            the number of arguments, the types of the formal parameters,
            and the return type are exactly the same in both definitions.
        '''
        for method in child_methods:
            print(method)
            if method.name in sig_parent:
                parent_signature = sig_parent[method.name]
                child_signature = sig_child[method.name]

                if parent_signature != child_signature:
                    raise SemantError(
                        "Redefined method %s cannot change arguments or \
                        return type, they must be the same of the parent \
                        method" % method.name
                    )

    def __add_method_from_parent_to_child(self, _cl, p_methods, c_methods):
        for method in p_methods:
            if method.name not in c_methods:
                copied_method = deepcopy(method)
                # Add at the beginning
                _cl.feature_list.insert(0, copied_method)

    def __add_attr_from_parent_to_child(self, _cl, attrs_of_parent):
        for attr in attrs_of_parent:
            # Add at the beginning
            _cl.feature_list.insert(0, deepcopy(attr))


def semant(ast):
    s = Semant(ast)
    s.build()
    print('\n\n====== CLASSES ======\n\n')
    print(s.classes)
    print('\n\n====== PARENTS ======\n\n')
    print(s.parents)
