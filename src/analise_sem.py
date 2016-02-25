from collections import defaultdict
from copy import deepcopy

from ast import *
from myexceptions import SemantError
from scope import Scope
from checktype import check_expression_type, returned_type


class Semant(object):
    """ Analyzes semantically the code. """

    def __init__(self, ast):
        self.ast = ast
        self.classes = {}
        self.parents = defaultdict(set)
        self.scope = Scope()

    def build(self):
        self.__create_default_classes()
        self.__create_symbol_tables()
        self.__check_undefined_classes()
        self.__check_inheritance_cycles()
        self.__check_inheritence_and_add_methods_in_children()

        for _class in self.classes.keys():
            self.__check_scope(self.classes[_class])

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
        # String inherits from Object
        stringc = Class("String", "Object", [
            Method('length', [], 'Int', None),
            Method('concat', [('arg', 'String')], 'String', None),
            Method(
                'substr', [('arg1', 'Int'), ('arg2', 'Int')], 'String', None
            ),
        ])

        self.ast += [objc, ioc, stringc]

    def __create_symbol_tables(self):
        """
            Create two tables:
            One with all the classes and another with all
            parents classes.
        """
        for _class in self.ast:
            if _class.name in self.classes:
                raise SemantError('Class %s already defined!' % _class.name)
            else:
                self.classes[_class.name] = _class

            if _class.name != 'Object':
                self.parents[_class.parent].add(_class.name)

    def __check_undefined_classes(self):
        """
            Check if every parent is defined in classes table. (self.classes)
        """
        parents = self.parents.keys()

        for parent in parents:
            if parent not in self.classes:
                class_name = self.parents[parent]
                message = 'Classe %s inherit from an undefined parent %s'

                raise SemantError(
                    message % (class_name, parent)
                )

    def __check_inheritance_cycles(self):
        """
            Check if every class has your right parent and children.

            First, set every class(including parents) as False.
            Then, visit each class and their childs.
        """
        visited = {}
        for parent_name in self.parents.keys():
            visited[parent_name] = False
            for child_name in self.parents[parent_name]:
                visited[child_name] = False

        # Visit every class, recursively, starting with Object
        self.__visit_tree('Object', visited)

        # If some class has False value, means that the visitor
        # couldn't get in that class. So, some class is missing.
        for key, value in visited.items():
            if not value:
                raise SemantError('%s is in a inheritance cycle' % key)

    def __visit_tree(self, _class, visited):
        visited[_class] = True

        # If a _class is not in parents,
        # it is not a parent, so, don't have children. Get out.
        if _class not in self.parents.keys():
            return

        for child in self.parents[_class]:
            self.__visit_tree(child, visited)

    def __check_inheritence_and_add_methods_in_children(self, _class='Object'):
        """
            Check attributes and methods from inheritance and
            if it is ok, add them from parent to child.
        """
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

        # Go recursively to all children
        all_children = self.parents[_class]
        for child in all_children:
            self.__check_inheritence_and_add_methods_in_children(child)

    def __get_attributes(self, _class):
        return [i for i in _class.feature_list if isAttribute(i)]

    def __check_same_attribute(self, parent, child):
        """
            It's illegal to redefine attribute names in child class.
        """
        for p_attr in parent:
            for c_attr in child:
                if p_attr.name == c_attr.name:
                    raise SemantError(
                        "Attribute cannot be redefined \
                        in child class %s" % cl.name
                    )

    def __get_methods(self, _class):
        return [i for i in _class.feature_list if isMethod(i)]

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
        """
            If a class "B" inherits a method "m" from an ancestor class "A",
            then "B" may override the inherited definition of "m" provided
            the number of arguments, the types of the formal parameters,
            and the return type are exactly the same in both definitions.
        """
        for method in child_methods:
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

    def __check_scope(self, _class):
        for feature in _class.feature_list:
            _type = returned_type(feature, _class)

            if isAttribute(feature):
                self.scope.add(feature.name, _type)

            elif isMethod(feature):
                self.scope.add(feature.name, (feature.formal_list, _type))
                self.__check_children_scope(feature.body, _class)

    def __check_children_scope(self, expression, _class):
        if isinstance(expression, Block):
            self.scope.new()

            for expr in expression.body:
                self.__check_children_scope(expr, _class)

            self.scope.destroy()

        elif isinstance(expression, Dispatch):
            self.__check_children_scope(expression.body, _class)

            # Get return type
            if expression.body == 'self':
                _class_name = _class.name
            else:
                _class_name = expression.body.return_type

            # Get the whole class' structure
            _class_content = self.classes[_class_name]

            called_method = False

            # Parse the structure untill match the method name
            for feature in _class_content.feature_list:
                if isMethod(feature) and feature.name == expression.method:
                    called_method = True

                    if len(feature.formal_list) != len(expression.expr_list):
                        msg = "Tried to call method %s in class %s with wrong number of arguments"
                        raise SemantError(
                            msg % (feature.name, _class_name)
                        )

                    formals = zip(
                        feature.formal_list, expression.expr_list,
                    )

                    for feat, called in formals:
                        # Test if the argument types are not equals
                        expression_type = check_expression_type(
                            called, _class, self.scope
                        )
                        # feat[0] is the name and feat[1] the type
                        if feat[1] != expression_type:
                            m = "Argument %s passed to method %s in class %s have a different type"
                            try:
                                # If is an Object, there is a name,
                                content_or_name = called.name
                            except AttributeError:
                                # if not, there is a content instead
                                content_or_name = called.content
                            raise SemantError(
                                m % (content_or_name, feature.name, _class_name)
                            )

                    # Test if the returns types are not equals
                    feature_type = _class_name
                    feature_type = returned_type(feature, _class)

                    if feature_type != feature_type:
                        msg = "The method %s in class %s returns wrong type"
                        raise SemantError(
                            msg % (feature.name, _class_name)
                        )
            # If didn't match the method name...
            if not called_method:
                msg = 'A undefined method %s was called in class %s'
                raise SemantError(msg % (expression.method, _class_name))


def isMethod(feature):
    return isinstance(feature, Method)


def isAttribute(feature):
    return isinstance(feature, Attr)


def semant(ast):
    print('\n\n====== DEBUGGING ======\n\n')
    s = Semant(ast)
    s.build()
    print('\n\n====== CLASSES ======\n\n')
    print(s.classes)
    print('\n\n====== PARENTS ======\n\n')
    print(s.parents)
