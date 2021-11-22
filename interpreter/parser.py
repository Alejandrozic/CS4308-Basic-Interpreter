"""
    The parser takes the expressions provided by a the Lexical Analyzer
    and is able to create statements.

    Error SyntaxErrorInvalidExpression happens when a invalid statement is
    entered.
"""

from interpreter.lexical_analyzer import LexicalAnalyzer
from interpreter.statements import *
from interpreter.runtime_errors import *


class Parser:

    def __init__(self, file: str):
        self.lexical_analyzer = LexicalAnalyzer(file)

    def run(self):
        while self.lexical_analyzer.scanner.is_eof is False:
            curr_line_num = self.lexical_analyzer.scanner.curr_line_num
            # Project Deliverable 3
            expression  = self.lexical_analyzer.get_next_expression()
            stmnt_class = statement_factory(expression)
            stmnt       = stmnt_class(expression)
            print(curr_line_num, stmnt.expr_tokens, stmnt.expr_values)
            try:
                stmnt.execute()
            except ProgramTermination:
                # -- Source Code requested Program termination
                # -- by using the "END" keyword.
                break
