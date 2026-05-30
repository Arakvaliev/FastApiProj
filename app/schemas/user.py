from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    login: str = Field(..., min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    login: Optional[str] = Field(None, min_length=3, max_length=50)

class UserRead(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)
    
    @field_validator('new_password')
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v