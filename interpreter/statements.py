"""
    Contains the supported statements as well as a statement_factory.

    Future implementation will include checking memory to ensure ID_TOK
    is found in memory table.
"""

from interpreter import memory
from interpreter.syntax_errors import *
from interpreter.runtime_errors import *
from interpreter.tokens import Tokens


class AssignmentStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """
            Assign Value to a Variable
        """
        index_of_id     = 0
        index_of_value  = 2
        memory.add_assignment(
            id_name=self.expression[index_of_id].value,
            value=self.expression[index_of_value].value,
        )


class CommentStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Nothing to Validate """
        pass

    def execute(self):
        """ No Action on Comment Statements """
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
        """ Terminate Execution of Program """
        raise ProgramTermination('')


class PrintStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ ID Token must be defined """
        if self.expression[-1].token_type == Tokens.ID_TOK:
            id_name = self.expression[-1].value
            if memory.get_assignment(id_name) is None:
                raise UndefinedVariableName(f'Variable Name "{id_name}" not defined.')

    def execute(self):
        """ Print the value of an ID Token """
        self.validate()
        if self.expression[-1].token_type == Tokens.ID_TOK:
            id_name = self.expression[-1].value
            value = memory.get_assignment(id_name)
        else:
            value = self.expression[-1].value
        print(value)


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
        id_name     = self.expression[-1].value
        question    = self.expression[-3].value
        value       = input(question+' ')

        # -- Check if input is an Integer -- #
        try:
            value = int(value)
        except ValueError:
            pass

        memory.add_assignment(
            id_name=id_name,
            value=value,
        )


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
        """ Implements Switch Logic for IF/ELSE """
        if self.conditional_statement.execute() is True:
            self.then_statement.execute()
        else:
            self.else_statement.execute()


class ConditionalStatement:

    def __init__(self, expression):
        self.expression = expression
        self.expr_tokens = [i.token_type.name for i in expression]
        self.expr_values = [i.value for i in expression]

    def validate(self):
        """ Validate ID tokens exists [where applicable] """
        left_expr = self.expression[0]
        if left_expr.token_type == Tokens.ID_TOK:
            id_name = left_expr.value
            if memory.get_assignment(id_name) is None:
                raise UndefinedVariableName(f'Variable Name "{id_name}" not defined.')
        right_expr = self.expression[2]
        if right_expr.token_type == Tokens.ID_TOK:
            id_name = right_expr.value
            if memory.get_assignment(id_name) is None:
                raise UndefinedVariableName(f'Variable Name "{id_name}" not defined.')

    def execute(self):
        """ Perform arithmetic condition check """
        left_expr       = self.expression[0]
        operator_expr   = self.expression[1]
        right_expr      = self.expression[2]
        # -- Pull Left side value from memory if ID Token -- #
        if left_expr.token_type == Tokens.ID_TOK:
            left_value = memory.get_assignment(left_expr.value)
        else:
            left_value = left_expr.value
        # -- Pull Right side value from memory if ID Token -- #
        if right_expr.token_type == Tokens.ID_TOK:
            right_value = memory.get_assignment(right_expr.value)
        else:
            right_value = right_expr.value
        # -- Operator Logic -- #
        if operator_expr.token_type == Tokens.GT_TOK:
            return left_value > right_value
        elif operator_expr.token_type == Tokens.LT_TOK:
            return left_value < right_value
        else:
            # -- Unsupported operator will get caught by the Parser -- #
            pass


def statement_factory(expression: list):
    """ Given an expression finds a appropriate STATEMENT Class [if available]"""
    expr_tokens = str([i.token_type.name for i in expression])

    if all([e in expr_tokens for e in ('IF_TOK', 'THEN_TOK', 'ELSE_TOK')]) and \
            expr_tokens.index('IF_TOK') < expr_tokens.index('THEN_TOK') < expr_tokens.index('ELSE_TOK'):
        return IfElseStatement

    mapping = {
        str(['ID_TOK', 'ASSIGN_TOK', 'CONST_STR_TOK'])              : AssignmentStatement,
        str(['ID_TOK', 'ASSIGN_TOK', 'CONST_INT_TOK'])              : AssignmentStatement,
        str(['INPUT_TOK', 'CONST_STR_TOK', 'COMMA_TOK', 'ID_TOK'])  : InputStatement,
        str(['REM_TOK', 'CONST_STR_TOK'])                           : CommentStatement,
        str(['PRINT_TOK', 'ID_TOK'])                                : PrintStatement,
        str(['PRINT_TOK', 'CONST_INT_TOK'])                         : PrintStatement,
        str(['PRINT_TOK', 'CONST_STR_TOK'])                         : PrintStatement,
        str(['ID_TOK', 'LT_TOK', 'CONST_INT_TOK'])                  : ConditionalStatement,
        str(['ID_TOK', 'LT_TOK', 'CONST_STR_TOK'])                  : ConditionalStatement,
        str(['ID_TOK', 'GT_TOK', 'CONST_INT_TOK'])                  : ConditionalStatement,
        str(['ID_TOK', 'GT_TOK', 'CONST_STR_TOK'])                  : ConditionalStatement,
        str(['END_TOK'])                                            : EndStatement,
    }

    try:
        return mapping[expr_tokens]
    except KeyError:
        # Invalid Expression
        expr_values = ' '.join([str(i.value) for i in expression])
        raise SyntaxErrorInvalidExpression(f"Expression '{expr_values}' is not valid")
