"""
    Unused.
    Reserved for future implementation of Interpreter component.
"""


class Memory:

    def __init__(self):
        self.table = dict()

    def add_assignment(self, id_name, value):
        self.table[id_name] = value
