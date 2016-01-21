from collections import namedtuple

# Used to create abstract syntax tree
Class = namedtuple("Class", "name, parent, feature_list")
Attr = namedtuple("Attr", "name, type, body")
Method = namedtuple(
    "Method", "name, formal_list, return_type, body"
)
Object = namedtuple("Object", "name")
Int = namedtuple("Int", "content")
Bool = namedtuple("Bool", "content")
Str = namedtuple("Str", "content")
Block = namedtuple("Block", "body")
Assign = namedtuple("Assign", "name, body")
Dispatch = namedtuple("Dispatch", "body, method, expr_list")
StaticDispatch = namedtuple(
    "StaticDispatch", "body, type, method, expr_list"
)
Plus = namedtuple("Plus", "first, second")
Sub = namedtuple("Sub", "first, second")
Mult = namedtuple("Mult", "first, second")
Div = namedtuple("Div", "first, second")
Lt = namedtuple("Lt", "first, second")
Le = namedtuple("Le", "first, second")
Eq = namedtuple("Eq", "first, second")
If = namedtuple("If", "predicate, then_body, else_body")
While = namedtuple("While", "predicate, body")
Case = namedtuple("Case", "expr, case_list")
New = namedtuple("New", "type")
Isvoid = namedtuple("Isvoid", "body")
Neg = namedtuple("Neg", "body")
Not = namedtuple("Not", "body")
