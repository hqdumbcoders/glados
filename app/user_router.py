from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.user_service import UserService
from app.exceptions import UserAlreadyExistsError, UserNotFoundError

router = APIRouter()

@router.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.create_user(
            username=user.username, 
            password=user.password,
            telegram_id=user.telegram_id
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this telegram_id already exists"
        )

@router.get("/api/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user(user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

@router.get("/status")
def get_status():
    return {"status": "OK"}