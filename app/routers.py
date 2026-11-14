from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AccountCreate, AccountResponse
from app.account_service import AccountService
from app.exceptions import AccountAlreadyExistsError, AccountNotFoundError

router = APIRouter()

@router.post("/api/v1/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    service = AccountService(db)
    try:
        return service.create_account(
            username=account.username,
            telegram_id=account.telegram_id
        )
    except AccountAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this telegram_id already exists"
        )

@router.get("/api/v1/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, db: Session = Depends(get_db)):
    service = AccountService(db)
    try:
        return service.get_account(account_id)
    except AccountNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

@router.get("/status")
def get_status():
    return {"status": "OK"}