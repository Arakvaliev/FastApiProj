from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.vacancy import CategoryRead

class ResumeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., pattern='^(male|female|other)$')
    age: int = Field(..., ge=18, le=100)
    phone: str = Field(..., pattern='^\+?[\d\s\-\(\)]{7,20}$')
    email: str = Field(..., pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    experience_years: int = Field(..., ge=0)
    higher_education: bool = False
    vacancy_id: Optional[int] = None
    category_id: int
    status: str = Field(default="new", pattern='^(new|in_progress|interviewed|hired|rejected)$')

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, pattern='^(male|female|other)$')
    age: Optional[int] = Field(None, ge=18, le=100)
    phone: Optional[str] = Field(None, pattern='^\+?[\d\s\-\(\)]{7,20}$')
    email: Optional[str] = Field(None, pattern='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    experience_years: Optional[int] = Field(None, ge=0)
    higher_education: Optional[bool] = None
    vacancy_id: Optional[int] = None
    category_id: Optional[int] = None
    status: Optional[str] = Field(None, pattern='^(new|in_progress|interviewed|hired|rejected)$')

class CategorySimple(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class ResumeListItem(BaseModel):
    id: int
    first_name: str
    last_name: str
    experience_years: int
    higher_education: bool
    category: CategorySimple
    vacancy_title: Optional[str] = None
    status: str
    
    model_config = ConfigDict(from_attributes=True)

class ResumeRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender: str
    age: int
    phone: str
    email: str
    experience_years: int
    higher_education: bool
    vacancy_id: Optional[int] = None
    category_id: int
    status: str
    created_at: datetime
    category: CategorySimple
    vacancy_title: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)