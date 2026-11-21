from sqlalchemy.orm import Session
from app.account_repository import AccountRepository
from app.models import Account
from app.exceptions import AccountAlreadyExistsError, AccountNotFoundError
from app.security import get_password_hash

class AccountService:
    def __init__(self, db: Session):
        self.repository = AccountRepository(db)

    def create_account(self, username: str, password: str, telegram_id: int | None = None) -> Account:
        if telegram_id is not None:
            existing = self.repository.get_by_telegram_id(telegram_id)
            if existing:
                raise AccountAlreadyExistsError()

        hashed_pwd = get_password_hash(password)
        return self.repository.create(username=username, hashed_password=hashed_pwd, telegram_id=telegram_id)

    def get_account(self, external_id: str) -> Account:
        account = self.repository.get_by_id(external_id)
        if account is None:
            raise AccountNotFoundError()

        return account