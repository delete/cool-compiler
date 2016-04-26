from ..syntactic.ast import *
from myexceptions import SemantError


def returned_type(feature, _class):
    """
        Returns the type of the feature.

        There is a difference between attribute and method.
        Attributes has "type" attribute and
        method has "return_type" attribute.
    """
    try:
        # For Attribute
        _type = feature.type
    except AttributeError:
        # For Method
        _type = feature.return_type

    if _type == 'SELF_TYPE':
        _type = _class.name

    return _type


def get_expression_type(expression, _class, scope):
    """
        Returns the type of the expression.

        If the type is self, then returns the name of the
        class.
    """
    if isinstance(expression, Str):
        return 'String'

    elif isinstance(expression, Object):
        if expression.name == "self":
            return _class.name

        if not scope.exists(expression.name):
            raise SemantError(
                "Variable %s is not in scope" % expression.name
            )

        return scope.get(expression.name)

    elif isinstance(expression, Int):
        return "Int"

    elif isinstance(expression, Bool):
        return "Bool"

    elif isinstance(expression, New):
        return returned_type(expression, _class)


def isMethod(feature):
    return isinstance(feature, Method)


def isAttribute(feature):
    return isinstance(feature, Attr)
