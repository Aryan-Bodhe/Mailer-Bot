class UserNotFound(Exception):
    def __init__(self, email: str):
        message = f"User {email} not found."
        super().__init__(message)

class UserAlreadyExists(Exception):
    def __init__(self, email: str):
        message = f"User {email} already exists."
        super().__init__(message)