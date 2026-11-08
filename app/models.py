import uuid
from sqlalchemy import Column, String, BigInteger
from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(String, primary_key = True, default = lambda: str(uuid.uuid4()))
    username = Column(String, unique = True, nullable = False)
    telegram_id = Column(BigInteger, unique = True, nullable = True)