from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AccountCreate, AccountResponse
from app import repository
import uuid

router = APIRouter()

@router.post("/api/v1/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)

def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    if account.telegram_id is not None:
        existing_tg = repository.get_account_by_telegram_id(db, account.telegram_id)
        if existing_tg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account with this telegram_id already exists"
            )

    new_id = str(uuid.uuid4())
    return repository.create_account(
        db=db,
        account_id=new_id,
        username=account.username,
        telegram_id=account.telegram_id
    )

@router.get("/api/v1/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: str, db: Session = Depends(get_db)):
    db_account = repository.get_account_by_id(db, account_id)
    if db_account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return db_account