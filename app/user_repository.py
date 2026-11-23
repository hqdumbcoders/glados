from sqlalchemy.orm import Session
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.query(User).filter(User.external_id == user_id).first()

    def get_by_pk(self, pk: int) -> User | None:
        return self.db.query(User).filter(User.id == pk).first()

    def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return self.db.query(User).filter(User.telegram_id == telegram_id).first()

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, username: str, hashed_password: str, telegram_id: int | None = None) -> User:
        db_user = User(
            username=username,
            hashed_password=hashed_password,
            telegram_id=telegram_id
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user