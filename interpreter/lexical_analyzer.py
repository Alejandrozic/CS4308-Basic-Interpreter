import interpreter.scanner
from interpreter.tokens import Tokens
from interpreter.syntax_errors import *


class LexicalAnalyzer:

    WHITESPACE = ' '
    QUOTE = '"'

    def __init__(self, file: str):
        self.scanner = interpreter.scanner.Scanner(file=file)
        self.token = []

    def run(self):
        while self.scanner.is_eof is False:
            line = self.scanner.get_next()
            lexemes = self.parse_lexemes(line)
            # -- Project Deliverable 1 -- #
            print('------------Line--------------')
            print(f'{line}')
            print('-------Scanned Tokens---------')
            for lexeme in lexemes:
                print('{0: <16} {1: <16}'.format(lexeme.token_type.name, lexeme.value))
            print('\n')

    def parse_lexemes(self, line: str):
        """ Iterates through each char in a line and parses out lexemes """
        lexemes = list()
        lexeme = ''
        line = list(line)
        while line:
            # Get next character
            char = line.pop(0)
            self.validate_char(char)
            # If character is WHITESPACE, submit LEXEME and restart
            if char == self.WHITESPACE:
                lexemes.append(lexeme)
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
                lexemes.append('"'+lexeme+'"')
                lexeme = ''
                continue
            lexeme += char
        # Add last one if not empty
        lexemes.append(lexeme)
        # Return non-empty lexemes
        # ignore the first lexeme as this is the line number
        return [Lexeme(l) for l in lexemes[1:] if l]

    def validate_char(self, char: str):
        """ Ensure terminal (char) is supported """
        if char.isalpha() or char.isalnum():
            return True
        elif char == self.WHITESPACE or char == self.QUOTE:
            return True
        elif char in ('=', ',', '<', '>'):
            return True
        raise SyntaxErrorInvalidCharacter(f'Invalid Character "{char}" at line {self.scanner.curr_line_num}')


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
        elif self.value.startswith(LexicalAnalyzer.QUOTE) and self.value.endswith(LexicalAnalyzer.QUOTE):
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
