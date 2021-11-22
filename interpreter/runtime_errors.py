class ProgramTermination(Exception):
    """ Program Termination was requested by Source Code """
    pass


class UndefinedVariableName(Exception):
    """ Variable access was attempted before variable assignment """
    pass
