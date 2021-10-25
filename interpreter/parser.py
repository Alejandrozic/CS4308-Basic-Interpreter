"""
    The parser takes the expressions provided by a the Lexical Analyzer
    and is able to create statements.

    Error SyntaxErrorInvalidExpression happens when a invalid statement is
    entered.
"""

from interpreter.lexical_analyzer import LexicalAnalyzer
from interpreter.statements import *


class Parser:

    def __init__(self, file: str):
        self.lexical_analyzer = LexicalAnalyzer(file)

    def run(self):
        while self.lexical_analyzer.scanner.is_eof is False:
            # Project Deliverable 2
            expression = self.lexical_analyzer.get_next_expression()
            stmnt_class = statement_factory(expression)
            stmnt = stmnt_class(expression)
            print(stmnt_class)
            print(stmnt.expr_tokens)
            print(stmnt.expr_values)
            print('\n')
