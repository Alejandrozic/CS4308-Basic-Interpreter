"""
    Implementation of Lexical Analysis
        - Interacts with Scanner to iterate through characters
        - Creates an Expression (list of lexemes) by line
"""

from interpreter.scanner import Scanner
from interpreter.syntax_errors import *
from interpreter.lexeme import Lexeme


class LexicalAnalyzer:

    WHITESPACE = ' '
    QUOTE = '"'

    def __init__(self, file: str):
        self.scanner = Scanner(file=file)

    def get_next_expression(self):
        line = self.scanner.get_next()
        return self.generate_expression(line)

    def generate_expression(self, line: str):
        """ Iterates through each char in a line and parses out lexemes """
        expression = list()
        lexeme = ''
        line = list(line)
        while line:
            # Get next character
            char = line.pop(0)
            self.validate_char(char)
            # If character is WHITESPACE, submit LEXEME and restart
            if char == self.WHITESPACE:
                expression.append(lexeme)
                lexeme = ''
                continue
            # If character starts with quotes, parse the until
            # the closing quote.
            if char == self.QUOTE:
                # Check for SYNTAX ERROR
                if self.QUOTE not in line:
                    raise SyntaxErrorMissingEndingQuote(
                        f'Missing ending quote at line {self.scanner.curr_line_num}.'
                    )
                while line:
                    char = line.pop(0)
                    self.validate_char(char)
                    if char == self.QUOTE:
                        break
                    lexeme += char
                expression.append('"'+lexeme+'"')
                lexeme = ''
                continue
            lexeme += char
        # Add last one if not empty
        expression.append(lexeme)
        # Return non-empty lexemes
        # ignore the first lexeme as this is the line number
        return [Lexeme(l) for l in expression[1:] if l]

    def validate_char(self, char: str):
        """ Ensure terminal (char) is supported """
        if char.isalpha() or char.isalnum():
            return True
        elif char == self.WHITESPACE or char == self.QUOTE:
            return True
        elif char in ('=', ',', '<', '>'):
            return True
        raise SyntaxErrorInvalidCharacter(f'Invalid Character "{char}" at line {self.scanner.curr_line_num}')
