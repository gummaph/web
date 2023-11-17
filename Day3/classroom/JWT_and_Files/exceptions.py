class BaseExceptions(Exception):

    def __init__(self, status, message):
        super().__init__()
        self.status = status
        self.message = message

    def __str__(self):
        return str({
            "status": self.status,
            "message": self.message
        })


class InvalidData(BaseExceptions):
    def __init__(self):
        super().__init__(400, "invalid data")


class IncorrectPassword(BaseExceptions):
    def __init__(self):
        super().__init__(401, "invalid credentials")

class InvalidToken(BaseExceptions):
    def __init__(self):
        super().__init__(400, "invalid Token")

class InsufficientPrivilage(BaseExceptions):
    def __init__(self):
        super().__init__(403, "insufficient privilege")