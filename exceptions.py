class UnknownCommand(Exception):
    def __init__(self, message = "Unknown command, try again"):
        super().__init__(message)

class NoneFound(Exception):
    def __init__(self, message = "Nothing Found."):
        super().__init__(message)

class Exit(Exception):
    def __init__(self, message = "EXIT"):
        super().__init__(message)

