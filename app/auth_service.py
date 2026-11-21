from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from app.account_repository import AccountRepository
from app.security import verify_password, create_access_token, create_refresh_token
from app.exceptions import InvalidCredentialsError, InvalidTokenError
from app.models import RefreshToken
from app.config import settings

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = AccountRepository(db)

    def login(self, username: str, password: str) -> dict:
        account = self.repository.get_by_username(username)
        if not account or not verify_password(password, account.hashed_password):
            raise InvalidCredentialsError

        token_data = {"sub": account.external_id, "role": account.role}
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)

        db_token = RefreshToken(
            token=refresh_token,
            account_id=account.id,
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.db.add(db_token)
        self.db.commit()

        return{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def logout(self, refresh_token: str):
        db_token = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if db_token:
            db_token.is_revoked = True
            self.db.commit()

    def refrehs_access_token(self, refresh_token: str) -> dict:
        db_token = self.db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if not db_token or db_token.is_revoked:
            raise InvalidTokenError()

        if db_token.expires_at < datetime.now(timezone.utc):
            raise InvalidTokenError()

        account = self.repository.get_by_pk(db_token.account_id)
        if not account:
            raise InvalidTokenError()

        token_data = {"sub": account.external_id, "role": account.role}
        new_access_token = create_access_token(data=token_data)

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }