from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class StudentBase(BaseModel):
    surname: str
    name: str
    faculty: str
    course: int = Field(ge=1, le=6)
    grade: float = Field(ge=0, le=100)

    @field_validator('surname', 'name')
    def validate_names(cls, v):
        if not re.match(r'^[А-Я][а-я]+$', v):
            raise ValueError('Должно содержать только кириллицу и заглавную первую букву')
        return v

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[int] = Field(None, ge=1, le=6)
    grade: Optional[float] = Field(None, ge=0, le=100)

class StudentResponse(StudentBase):
    id: int
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None