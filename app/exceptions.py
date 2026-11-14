class AccountAlreadyExistsError(Exception):
    """Raised when trying to create an account with a duplicate telegram_id."""
    pass

class AccountNotFoundError(Exception):
    """Raised when an account is not found in the database."""
    pass