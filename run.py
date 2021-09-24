"""
Tested with Python 3.6.4
"""

import sys
import interpreter.lexical_analyzer


def main():
    lexical_analyzer = interpreter.lexical_analyzer.LexicalAnalyzer(file)
    lexical_analyzer.run()


if __name__ == '__main__':
    try:
        # Try to get the file as a argument
        file = sys.argv[1]
    except IndexError:
        # If no arguments are passed, use the default
        file = 'source_files/example1.bas'
    main()
