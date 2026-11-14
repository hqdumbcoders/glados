from sqlalchemy.orm import Session
from app.models import Account

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id: str) -> Account | None:
        return self.db.query(Account).filter(Account.external_id == account_id).first()

    def get_by_telegram_id(self, telegram_id: int) -> Account | None:
        return self.db.query(Account).filter(Account.telegram_id == telegram_id).first()

    def create(self, username: str, telegram_id: int | None = None) -> Account:
        db_account = Account(
            username=username,
            telegram_id=telegram_id
        )

        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account