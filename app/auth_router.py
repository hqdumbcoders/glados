from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import LoginRequest, Token, RefreshRequest, LogoutRequest
from app.auth_service import AuthService
from app.exceptions import InvalidTokenError, InvalidCredentialsError

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.login(username=login_data.username, password=login_data.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

@router.post("/refresh")
def refresh_token(data: RefreshRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    try:
        return service.refrehs_access_token(data.refresh_token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

@router.post("/logout")
def logout(data: LogoutRequest, db: Session = Depends(get_db)):
    service = AuthService(db)
    service.logout(data.refresh_token)
    return {"status": "OK"}