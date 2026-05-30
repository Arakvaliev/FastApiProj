from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead, PasswordChange
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.auth_service = AuthService(db)
    
    def create_user(self, user_data: UserCreate) -> UserRead:
        existing_user = self.user_repo.get_by_login(user_data.login)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login already registered"
            )
        
        hashed_password = self.auth_service.hash_password(user_data.password)
        
        user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            login=user_data.login,
            hashed_password=hashed_password
        )
        
        created_user = self.user_repo.create(user)
        return UserRead.model_validate(created_user)
    
    def login(self, login: str, password: str) -> dict:
        user = self.auth_service.authenticate_user(login, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token = self.auth_service.create_access_token(data={"sub": str(user.id)})
        refresh_token = self.auth_service.create_refresh_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def change_password(self, user: User, password_data: PasswordChange) -> dict:
        if not self.auth_service.verify_password(password_data.old_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password"
            )
        
        new_hashed_password = self.auth_service.hash_password(password_data.new_password)
        self.user_repo.update_password(user, new_hashed_password)
        
        return {"message": "Password changed successfully"}