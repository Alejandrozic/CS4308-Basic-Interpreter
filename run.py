"""
    Tested on Python 3.6.4 and Python 3.7.4
"""

import sys
from interpreter.parser import Parser


def main():
    parser = Parser(file)
    parser.run()


if __name__ == '__main__':
    try:
        # Try to get the file as a argument
        file = sys.argv[1]
    except IndexError:
        # If no arguments are passed, use the default
        file = 'source_files/example2.bas'
    main()
