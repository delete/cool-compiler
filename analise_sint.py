import ply.yacc as yacc

from tokrules import tokens
from ast import *
from analise_lex import MyLex


def syntactic(string):

    def p_class_list_many(p):
        '''class_list : class_list class SEMI'''
        p[0] = p[1] + [p[2]]

    def p_class_list_single(p):
        '''class_list : class SEMI'''
        p[0] = [p[1]]

    def p_class(p):
        '''class : CLASS TYPEID LBRACE feature_list RBRACE'''
        p[0] = Class(p[2], "Object", p[4])

    def p_class_inherits(p):
        '''class : CLASS TYPEID INHERITS TYPEID LBRACE feature_list RBRACE'''
        p[0] = Class(p[2], p[4], p[6])

    def p_feature_list_many(p):
        '''feature_list : feature_list feature SEMI'''
        p[0] = p[1] + [p[2]]

    def p_feature_list_single(p):
        '''feature_list : feature SEMI'''
        p[0] = [p[1]]

    def p_feature_list_empty(p):
        '''feature_list : '''
        p[0] = []

    def p_feature_method(p):
        '''feature : OBJECTID LPAREN formal_list RPAREN COLON TYPEID LBRACE expression RBRACE'''
        p[0] = Method(p[1], p[3], p[6], p[8])

    def p_feature_method_no_formals(p):
        '''feature : OBJECTID LPAREN RPAREN COLON TYPEID LBRACE expression RBRACE'''
        p[0] = Method(p[1], [], p[5], p[7])

    def p_feature_attr_initialized(p):
        '''feature : OBJECTID COLON TYPEID ASSIGN expression'''
        p[0] = Attr(p[1], p[3], p[5])

    def p_feature_attr(p):
        '''feature : OBJECTID COLON TYPEID'''
        p[0] = Attr(p[1], p[3], None)

    def p_formal_list_many(p):
        '''formal_list : formal_list COMMA formal'''
        p[0] = p[1] + [p[3]]

    def p_formal_list_single(p):
        '''formal_list : formal'''
        p[0] = [p[1]]

    def p_formal(p):
        '''formal : OBJECTID COLON TYPEID'''
        p[0] = (p[1], p[3])

    def p_expression_object(p):
        '''expression : OBJECTID'''
        p[0] = Object(p[1])

    def p_expression_int(p):
        '''expression : INT_CONST'''
        p[0] = Int(p[1])

    def p_expression_bool(p):
        '''expression : BOOL_CONST'''
        p[0] = Bool(p[1])

    def p_expression_str(p):
        '''expression : STR_CONST'''
        p[0] = Str(p[1])

    def p_expression_block(p):
        '''expression : LBRACE block_list RBRACE'''
        p[0] = Block(p[2])

    def p_block_list_many(p):
        '''block_list : block_list expression SEMI'''
        p[0] = p[1] + [p[2]]

    def p_block_list_single(p):
        '''block_list : expression SEMI'''
        p[0] = [p[1]]

    def p_expression_assignment(p):
        '''expression : OBJECTID ASSIGN expression'''
        p[0] = Assign(Object(p[1]), p[3])

    def p_expression_dispatch(p):
        '''expression : expression DOT OBJECTID LPAREN expr_list RPAREN'''
        p[0] = Dispatch(p[1], p[3], p[5])

    def p_expr_list_many(p):
        '''expr_list : expr_list COMMA expression'''
        p[0] = p[1] + [p[3]]

    def p_expr_list_single(p):
        '''expr_list : expression'''
        p[0] = [p[1]]

    def p_expr_list_empty(p):
        '''expr_list : '''
        p[0] = []

    def p_expression_static_dispatch(p):
        '''expression : expression AT TYPEID DOT OBJECTID LPAREN expr_list RPAREN'''
        p[0] = StaticDispatch(p[1], p[3], p[5], p[7])

    def p_expression_self_dispatch(p):
        '''expression : OBJECTID LPAREN expr_list RPAREN'''
        p[0] = Dispatch("self", p[1], p[3])

    def p_expression_basic_math(p):
        '''
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression MULT expression
                   | expression DIV expression
        '''
        if p[2] == '+':
            p[0] = Plus(p[1], p[3])
        elif p[2] == '-':
            p[0] = Sub(p[1], p[3])
        elif p[2] == '*':
            p[0] = Mult(p[1], p[3])
        elif p[2] == '/':
            p[0] = Div(p[1], p[3])

    def p_expression_numerical_comparison(p):
        '''
        expression : expression LT expression
                   | expression LE expression
                   | expression EQ expression
        '''
        if p[2] == '<':
            p[0] = Lt(p[1], p[3])
        elif p[2] == '<=':
            p[0] = Le(p[1], p[3])
        elif p[2] == '=':
            p[0] = Eq(p[1], p[3])

    def p_expression_with_parenthesis(p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[2]

    def p_expression_if(p):
        '''expression : IF expression THEN expression ELSE expression FI'''
        p[0] = If(p[2], p[4], p[6])

    def p_expression_while(p):
        '''expression : WHILE expression LOOP expression POOL'''
        p[0] = While(p[2], p[4])

    def p_expression_case(p):
        '''expression : CASE expression OF case_list ESAC'''
        p[0] = Case(p[2], p[4])

    def p_case_list_one(p):
        '''case_list : case'''
        p[0] = [p[1]]

    def p_case_list_many(p):
        '''case_list : case_list case'''
        p[0] = p[1] + [p[2]]

    def p_case_expr(p):
        '''case : OBJECTID COLON TYPEID DARROW expression SEMI'''
        p[0] = (p[1], p[3], p[5])

    def p_expression_new(p):
        '''expression : NEW TYPEID'''
        p[0] = New(p[2])

    def p_expression_isvoid(p):
        '''expression : ISVOID expression'''
        p[0] = Isvoid(p[2])

    def p_expression_neg(p):
        '''expression : NEG expression'''
        p[0] = Neg(p[2])

    def p_expression_not(p):
        '''expression : NOT expression'''
        p[0] = Not(p[2])

    precedence = (
        ('right', 'ASSIGN'),
        ('left', 'NOT'),
        ('nonassoc', 'LE', 'LT', 'EQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV'),
        ('left', 'ISVOID'),
        ('left', 'NEG'),
        ('left', 'AT'),
        ('left', 'DOT'),
    )

    serror = []

    # Error rule for syntax errors
    def p_error(p):
        er = (p.type, p.value[0], p.lineno, p.lexpos)
        serror.append(er)
        print('parser error: {}'.format(p))

    # Build the parser
    parser = yacc.yacc()

    l = MyLex()
    lexer = l.lexer

    result = parser.parse(string, lexer=lexer)

    return result, serror


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            data = file.read()

        result, errors = syntactic(data)
        if result:
            print('\nOK!\n')
            #print(result)
    else:
        print('A cool file is required.')