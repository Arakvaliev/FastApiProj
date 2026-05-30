from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import (
    UserCreate, UserRead, UserLogin, Token, 
    TokenRefresh, PasswordChange)
from app.services.user_service import UserService
from app.services.auth_service import get_current_user, AuthService
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.login(login_data.login, login_data.password)

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(token_data.refresh_token)

@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_service = UserService(db)
    return user_service.change_password(current_user, password_data)

@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user