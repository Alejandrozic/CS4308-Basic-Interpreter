"""
    Opens file into memory and provides:
        - Function to get next line
        - Variable to determine if end of file has been reached
"""


class Scanner:

    def __init__(self, file: str):
        self.curr_line_num  = 0
        self.is_eof         = False
        self.file           = open(file, 'r')
        self.lines          = self.file.read().splitlines()

    def __del__(self):
        # -- This closes file handle when the garbage collector
        # -- is cleaning up this class.
        self.file.close()

    def get_next(self) -> str:
        """
        Retrieves next line item in the input file.
        """
        line = self.lines[self.curr_line_num]
        self.curr_line_num += 1
        self.__update_is_eof__()
        return line

    def __update_is_eof__(self):
        """
        Updates the self.is_eof (is end of file) variable
        if the current line number is greater then or equal to
        the total number of lines.
        """
        if self.curr_line_num >= len(self.lines):
            self.is_eof = True
