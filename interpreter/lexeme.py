"""
    Implements a Lexeme Object. It consists of a raw value
    and a predefined Token Type.
"""

from interpreter.tokens import Tokens
from interpreter.syntax_errors import *

QUOTE = '"'


class Lexeme:

    def __init__(self, value: str):
        self.value = value
        self.token_type = self.set_token_type()

    def set_token_type(self):
        if self.value.upper() == 'REM':
            return Tokens.REM_TOK
        elif self.value.upper() == 'INPUT':
            return Tokens.INPUT_TOK
        elif self.value.upper() == 'PRINT':
            return Tokens.PRINT_TOK
        elif self.value.upper() == 'END':
            return Tokens.END_TOK
        elif self.value.upper() == '=':
            return Tokens.ASSIGN_TOK
        elif self.value.upper() == '>':
            return Tokens.GT_TOK
        elif self.value.upper() == '<':
            return Tokens.LT_TOK
        elif self.value.upper() == ',':
            return Tokens.COMMA_TOK
        elif self.value.upper() == 'IF':
            return Tokens.IF_TOK
        elif self.value.upper() == 'THEN':
            return Tokens.THEN_TOK
        elif self.value.upper() == 'ELSE':
            return Tokens.ELSE_TOK
        elif self.value.startswith(QUOTE) and self.value.endswith(QUOTE):
            return Tokens.CONST_STR_TOK
        elif self.is_integer():
            return Tokens.CONST_INT_TOK
        elif self.value.isalpha():
            return Tokens.ID_TOK

    def is_integer(self) -> bool:
        """ Checks if Lexeme value is a number """
        if self.value.isnumeric():
            if self.value != '0' and self.value.startswith('0'):
                raise SyntaxErrorInvalidInteger(
                    f'Integer "{self.value}" cannot start with a zero unless the value is exactly 0.'
                )
            self.value = int(self.value)
            return True
        return False
