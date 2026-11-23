class UserAlreadyExistsError(Exception):
    """Raised when trying to create an user with a duplicate telegram_id."""
    pass

class UserNotFoundError(Exception):
    """Raised when an user is not found in the database."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when login or password is incorrect."""
    pass

class InvalidTokenError(Exception):
    """Raised when a token is invalid, expired or revoked."""
    pass