from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    telegram_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserResponse(BaseModel):
    id: int
    external_id: str
    username: str
    first_name: str | None = None
    last_name: str | None = None
    role: str
    telegram_id: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str