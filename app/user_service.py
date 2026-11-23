from sqlalchemy.orm import Session
from app.user_repository import UserRepository
from app.models import User
from app.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.security import get_password_hash

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, username: str, password: str, telegram_id: int | None = None) -> User:
        if telegram_id is not None:
            existing = self.repository.get_by_telegram_id(telegram_id)
            if existing:
                raise UserAlreadyExistsError()
        
        hashed_pwd = get_password_hash(password)
        return self.repository.create(username=username, hashed_password=hashed_pwd, telegram_id=telegram_id)

    def get_user(self, external_id: str) -> User:
        user = self.repository.get_by_id(external_id)
        if user is None:
            raise UserNotFoundError()
        return user