from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class PositionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class PositionCreate(PositionBase):
    pass

class PositionRead(PositionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class VacancyBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    position_id: int
    category_id: int
    min_salary: int = Field(..., ge=0)

class VacancyCreate(VacancyBase):
    pass

class VacancyUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    position_id: Optional[int] = None
    category_id: Optional[int] = None
    status: Optional[str] = None
    min_salary: Optional[int] = Field(None, ge=0)

class VacancyListItem(BaseModel):
    id: int
    title: str
    category: str
    status: str
    min_salary: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class VacancyRead(VacancyBase):
    id: int
    status: str
    position: PositionRead
    category: CategoryRead
    hr_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)