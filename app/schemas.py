from pydantic import BaseModel

class AccountCreate(BaseModel):
    username: str
    telegram_id: int | None = None

class AccountResponse(BaseModel):
    id: str
    username: str
    telegram_id: int | None = None

    model_config = {"from_attributes": True}