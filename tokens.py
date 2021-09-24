"""
    This file defines the available Tokens.
"""

from enum import Enum, auto  # Enumeration functionality from the Standard Python Library


class Tokens(Enum):
    REM_TOK         = auto()  # REM
    INPUT_TOK       = auto()  # INPUT
    PRINT_TOK       = auto()  # PRINT
    END_TOK         = auto()  # END
    CONST_STR_TOK   = auto()  # CONSTANT (String)
    CONST_INT_TOK   = auto()  # CONSTANT (Number)
    ID_TOK          = auto()  # VARIABLE
    ASSIGN_TOK      = auto()  # =
    GT_TOK          = auto()  # >
    LT_TOK          = auto()  # <
    COMMA_TOK       = auto()  # ,
    IF_TOK          = auto()  # IF
    THEN_TOK        = auto()  # THEN
    ELSE_TOK        = auto()  # ELSE
