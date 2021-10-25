"""
    Contains the supported statements as well as a statement_factory.

    Future implementation will include checking memory to ensure ID_TOK
    is found in memory table.
"""

from interpreter import memory
from interpreter.syntax_errors import *


class AssignmentStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


class CommentStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


class EndStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


class PrintStatement:
    """
        Prints an ID Token.
    """
    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ ID Token must be defined """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


class InputStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


class IfElseStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

        self.conditional_statement = None
        self.then_statement = None
        self.else_statement = None
        self.find_nested_statements()

    def find_nested_statements(self):
        """ Find Condition, Pass Statement and Failure Statement"""
        if_index    = self.expr_tokens.index('IF_TOK')
        then_index  = self.expr_tokens.index('THEN_TOK')
        else_index  = self.expr_tokens.index('ELSE_TOK')

        condition = self.expression[if_index+1:then_index]
        match = self.expression[then_index+1:else_index]
        no_match = self.expression[else_index+1:]

        condition_class = statement_factory(expression=condition)
        match_class = statement_factory(expression=match)
        no_match_class = statement_factory(expression=no_match)

        self.conditional_statement = condition_class(expression=condition)
        self.then_statement = match_class(expression=match)
        self.else_statement = no_match_class(expression=no_match)

        self.expr_tokens = [self.expr_tokens[if_index]] + \
                           [str(condition_class.__name__)] + \
                           [self.expr_tokens[then_index]] + \
                           [str(match_class.__name__)] + \
                           [self.expr_tokens[else_index]] + \
                           [str(no_match_class.__name__)]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


class ConditionalStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ Reserved Interpreter component implementation """
        pass


def statement_factory(expression: list):
    """ Given an expression finds a appropriate STATEMENT Class [if available]"""
    expr_tokens = str([i.token_type.name for i in expression])

    if all([e in expr_tokens for e in ('IF_TOK', 'THEN_TOK', 'ELSE_TOK')]) and \
            expr_tokens.index('IF_TOK') < expr_tokens.index('THEN_TOK') < expr_tokens.index('ELSE_TOK'):
        return IfElseStatement

    mapping = {
        str(['ID_TOK', 'ASSIGN_TOK', 'CONST_STR_TOK']): AssignmentStatement,
        str(['ID_TOK', 'ASSIGN_TOK', 'CONST_INT_TOK']): AssignmentStatement,
        str(['INPUT_TOK', 'CONST_STR_TOK', 'COMMA_TOK', 'ID_TOK']): InputStatement,
        str(['REM_TOK', 'CONST_STR_TOK']): CommentStatement,
        str(['PRINT_TOK', 'ID_TOK']): PrintStatement,
        str(['PRINT_TOK', 'CONST_INT_TOK']): PrintStatement,
        str(['PRINT_TOK', 'CONST_STR_TOK']): PrintStatement,
        str(['ID_TOK', 'LT_TOK', 'CONST_INT_TOK']): ConditionalStatement,
        str(['ID_TOK', 'LT_TOK', 'CONST_STR_TOK']): ConditionalStatement,
        str(['ID_TOK', 'GT_TOK', 'CONST_INT_TOK']): ConditionalStatement,
        str(['ID_TOK', 'GT_TOK', 'CONST_STR_TOK']): ConditionalStatement,
        str(['END_TOK']): EndStatement,
    }

    try:
        return mapping[expr_tokens]
    except KeyError:
        # Invalid Expression
        expr_values = ' '.join([str(i.value) for i in expression])
        raise SyntaxErrorInvalidExpression(f"Expression '{expr_values}' is not valid")
