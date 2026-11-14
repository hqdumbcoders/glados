from pydantic import BaseModel
from datetime import datetime

class AccountCreate(BaseModel):
    username: str
    telegram_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None

class AccountResponse(BaseModel):
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