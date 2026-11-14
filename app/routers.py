from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AccountCreate, AccountResponse
from app.account_service import AccountService

router = APIRouter()

@router.post("/api/v1/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    service = AccountService(db)
    return service.create_account(
        username=account.username,
        telegram_id=account.telegram_id
    )

@router.get("/api/v1/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, db: Session = Depends(get_db)):
    service = AccountService(db)
    return service.get_account(account_id)

@router.get("/status")
def get_status():
    return {"status": "OK"}