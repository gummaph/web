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
        super().__init__(400,"invalid data")

