from sqlalchemy.orm import Session
from app.models import Account

def get_account_by_id(db: Session, account_id: str):
    return db.query(Account).filter(Account.id == account_id).first()

def get_account_by_telegram_id(db: Session, telegram_id: int):
    return db.query(Account).filter(Account.telegram_id == telegram_id).first()

def create_account(db: Session, account_id: str, username: str, telegram_id: int | None = None):
    db_account = Account(
        id = account_id,
        username = username,
        telegram_id = telegram_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account