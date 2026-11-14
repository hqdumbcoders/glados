from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.account_repository import AccountRepository
from app.models import Account

class AccountService:
    def __init__(self, db: Session):
        self.repository = AccountRepository(db)

    def create_account(self, username: str, telegram_id: int | None = None) -> Account:
        if telegram_id is not None:
            existing = self.repository.get_by_telegram_id(telegram_id)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account with this telegram_id already exists"
                )
        
        return self.repository.create(username=username, telegram_id=telegram_id)

    def get_account(self, external_id: str) -> Account:
        account = self.repository.get_by_id(external_id)
        if account is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )

        return account