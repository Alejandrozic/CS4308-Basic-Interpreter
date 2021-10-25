"""
    File contains the various SyntaxError that are
    checked by the Lexical Analyzer.
"""


class SyntaxErrorMissingEndingQuote(Exception):
    """ Start Quote is missing an end Quote """
    pass


class SyntaxErrorInvalidInteger(Exception):
    """ Integer is Invalid """
    pass


class SyntaxErrorInvalidCharacter(Exception):
    """ Character was not defined in our grammar and thus is not supported """
    pass


class SyntaxErrorInvalidExpression(Exception):
    """ Expression is not Valid [supported] """
    pass
