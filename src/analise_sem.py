from collections import defaultdict
from copy import deepcopy

from ast import *
from myexceptions import (
    UndefinedMethodError, ReturnedTypeError,
    NumberOfArgumentError, RedefinedMethodError, RedefinedAttributeError,
    UndefinedParentError, ClassAlreadyDefinedError, InheritanceError,
    ArgumentTypeError, DeclaredTypeError, AttributeTypeError,
    TypeCheckError, WhileStatementError, ArithmeticError, AssignError
)
from scope import Scope
from checktype import (
    get_expression_type, returned_type, isAttribute, isMethod
)


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
            self.__check_scope_and_type(self.classes[_class])

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
                raise ClassAlreadyDefinedError(_class.name)

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
                raise UndefinedParentError(class_name, parent)

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
                raise InheritanceError(key)

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

            self.__check_same_attribute(
                attrs_of_parent, attrs_of_child, _class
            )

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

        # Goes recursively to all children
        all_children = self.parents[_class]
        for child in all_children:
            self.__check_inheritence_and_add_methods_in_children(child)

    def __get_attributes(self, _class):
        return [i for i in _class.feature_list if isAttribute(i)]

    def __check_same_attribute(self, parent, child, _class):
        """
            It's illegal to redefine attribute names in child class.
        """
        for p_attr in parent:
            for c_attr in child:
                if p_attr.name == c_attr.name:
                    raise RedefinedAttributeError(_class)

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
                    raise RedefinedMethodError(method.name)

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

    def __check_scope_and_type(self, _class):
        """
            Check scope and type for each class.

            If it's a method, goes recursively inside the body.

            When a scope is created?
            With a new block, let, case,

            OBS: Every attribute is private and every method is public.
        """

        for feature in _class.feature_list:
            _type = returned_type(feature, _class)

            if isAttribute(feature):
                value_type = get_expression_type(
                    feature.body, _class, self.scope
                )
                # Test if the attribute value type is the same as declared.
                if feature.type != value_type:
                    raise AttributeTypeError(feature, value_type)

                self.scope.add(feature.name, _type)

            elif isMethod(feature):
                self.scope.add(feature.name, (feature.formal_list, _type))
                self.__check_children(feature.body, _class)

    def __check_children(self, expression, _class):
        if isinstance(expression, Block):
            self.scope.new()

            for expr in expression.body:
                self.__check_children(expr, _class)

            self.scope.destroy()

        elif isinstance(expression, Dispatch):
            self.__check_children(expression.body, _class)

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
                        raise NumberOfArgumentError(feature.name, _class_name)

                    formals = zip(
                        feature.formal_list, expression.expr_list,
                    )

                    # Test if the arguments types are not equals
                    for feat, called in formals:
                        expression_type = get_expression_type(
                            called, _class, self.scope
                        )
                        # feat[0] is the name and feat[1] the type
                        if feat[1] != expression_type:
                            raise ArgumentTypeError(feature, _class_name)

                    # Test if the returns types are not equals
                    called_method_type = _class_name
                    feature_type = returned_type(feature, _class)

                    if feature_type != called_method_type:
                        raise ReturnedTypeError(feature.name, _class_name)

            # If didn't match the method name...
            if not called_method:
                raise UndefinedMethodError(expression.method, _class_name)

        elif isinstance(expression, Let):
            self.scope.new()
            self.scope.add(expression.object, expression.type)

            # Test if the declared type is the same type as
            # the given value
            value_type = get_expression_type(
                expression.init, _class, self.scope
            )
            if expression.type != value_type:
                raise DeclaredTypeError(expression.type, value_type)

            self.__check_children(expression.body, _class)

            self.scope.destroy()

        elif isinstance(expression, While):
            self.__check_children(expression.predicate, _class)
            self.__check_children(expression.body, _class)

            # If the methods above did not raise an error, means that
            # the body type is Int or an Object.
            # If is an Object and is not a Bool, must raise an error.
            if isinstance(expression.predicate, Object):
                obj_type = get_expression_type(
                    expression.predicate, _class, self.scope
                )
                if obj_type != 'Bool':
                    raise WhileStatementError(obj_type, _class)

        elif isinstance(expression, Lt) or isinstance(expression, Le):
            first_type, second_type = self.__get_params_types(
                expression, _class
            )

            if first_type != 'Int' or second_type != 'Int':
                raise TypeCheckError(first_type, second_type, _class)

        elif any(isinstance(expression, X) for X in [Plus, Sub, Mult, Div]):
            first_type, second_type = self.__get_params_types(
                expression, _class
            )

            if first_type != 'Int' or second_type != 'Int':
                raise ArithmeticError(first_type, second_type, _class)

        elif isinstance(expression, Assign):
            self.__check_children(expression.body, _class)
            # If the method above did not raise an error, means that
            # the body type is Int. Just need to test name now type.
            name_type = get_expression_type(
                expression.name, _class, self.scope
            )

            if name_type != 'Int':
                raise AssignError(name_type, 'Int', _class)

    def __get_params_types(self, expression, _class):
        first_type = get_expression_type(
            expression.first, _class, self.scope
        )
        second_type = get_expression_type(
            expression.second, _class, self.scope
        )
        return first_type, second_type


def semant(ast):
    print('\n\n====== DEBUGGING ======\n\n')
    s = Semant(ast)
    s.build()
    print('\n\n====== CLASSES ======\n\n')
    print(s.classes)
    print('\n\n====== PARENTS ======\n\n')
    print(s.parents)
