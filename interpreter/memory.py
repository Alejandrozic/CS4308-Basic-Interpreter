"""
    Virtual Memory Component
"""


class Memory:

    def __init__(self):
        self.table = dict()

    def add_assignment(self, id_name, value):
        if isinstance(value, str):
            value = value.replace('"', '')
        self.table[id_name] = value

    def get_assignment(self, id_name):
        try:
            return self.table[id_name]
        except KeyError:
            return None

    def __str__(self):
        """ Function to print and visualize memory """
        return '\n'.join([
            'Memory Table',
            '-------START-------',
            *[
                f'{k}={v}'
                for k, v in self.table.items()
            ],
            '--------END--------',
        ])
