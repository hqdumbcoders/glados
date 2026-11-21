from sqlalchemy.orm import Session
from app.models import Account

class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, account_id: str) -> Account | None:
        return self.db.query(Account).filter(Account.external_id == account_id).first()

    def get_by_pk(self, pk: int) -> Account | None:
        return self.db.query(Account).filter(Account.id == pk).first()

    def get_by_telegram_id(self, telegram_id: int) -> Account | None:
        return self.db.query(Account).filter(Account.telegram_id == telegram_id).first()

    def get_by_username(self, username: str) -> Account | None:
        return self.db.query(Account).filter(Account.username == username).first()

    def create(self, username: str, hashed_password: str, telegram_id: int | None = None) -> Account:
        db_account = Account(
            username=username,
            hashed_password=hashed_password,
            telegram_id=telegram_id
        )

        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account