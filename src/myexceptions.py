class SemantError(Exception):
    pass


class UndefinedMethodError(SemantError):

    def __init__(self, method, _class):
        msg = 'A undefined method %s was called in class %s'
        super(UndefinedMethodError, self).__init__(msg % (method, _class))


class ReturnedTypeError(SemantError):

    def __init__(self, method, _class):
        msg = 'The method %s in class %s returns wrong type'
        super(ReturnedTypeError, self).__init__(msg % (method, _class))


class ArgumentTypeError(SemantError):

    def __init__(self, method, class_name):
        m = "Argument %s passed to method %s in class %s have a different type"
        try:
            # If is an Object, there is a name,
            content_or_name = method.name
        except AttributeError:
            # if not, there is a content instead
            content_or_name = method.content
        super(ArgumentTypeError, self).__init__(
            m % (content_or_name, method.name, class_name)
        )


class NumberOfArgumentError(SemantError):

    def __init__(self, method, _class):
        msg = 'Tried to call method %s in class %s with wrong number of arguments'
        super(NumberOfArgumentError, self).__init__(msg % (method, _class))


class RedefinedMethodError(SemantError):

    def __init__(self, method_nmae):
        msg = "Redefined method %s cannot change arguments or return type, they must be the same of the parent method"
        super(RedefinedMethodError, self).__init__(msg % (method_nmae))


class RedefinedAttributeError(SemantError):

    def __init__(self, class_nmae):
        msg = "Attribute cannot be redefined in child class %s"
        super(RedefinedAttributeError, self).__init__(msg % (class_nmae))


class UndefinedParentError(SemantError):

    def __init__(self, child, parent):
        msg = 'Classe %s inherit from an undefined parent %s'
        super(UndefinedParentError, self).__init__(msg % (child, parent))


class ClassAlreadyDefinedError(SemantError):

    def __init__(self, class_name):
        msg = 'Class %s already defined'
        super(ClassAlreadyDefinedError, self).__init__(msg % (class_name))


class InheritanceError(SemantError):

    def __init__(self, class_name):
        msg = '%s is in a inheritance cycle'
        super(InheritanceError, self).__init__(msg % (class_name))
