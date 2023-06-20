class RuntimeException(Exception):
    """
    Base interpreter exception.
    """

    def __init__(self, message: str):
        self.message = message


class VariableNotFoundException(RuntimeException):
    """
    Raises if variable is not found in Memory object.
    """

    def __init__(self, name: str):
        self.message = f"Variable '{name}' is not defined."


class TypingError(RuntimeException):
    """
    Raises in case of differences between expected and actual type.
    """

    pass


class NotImplementedException(RuntimeException):
    """
    Raises when evaluated instruction has not yet implemented.
    """

    def __init__(self, instruction):
        self.message = f"{instruction} is not implemented."
