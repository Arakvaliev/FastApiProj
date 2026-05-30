from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text, Integer, Boolean, DateTime, func
from datetime import datetime, timezone
from typing import Optional
from app.core.database import Base

class Position(Base):
    __tablename__ = "positions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="position")

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="category")
    resumes: Mapped[list["Resume"]] = relationship(back_populates="category")

class Vacancy(Base):
    __tablename__ = "vacancies"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="open", nullable=False)
    min_salary: Mapped[int] = mapped_column(Integer, nullable=False)
    hr_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )
    
    position: Mapped["Position"] = relationship(back_populates="vacancies")
    category: Mapped["Category"] = relationship(back_populates="vacancies")
    hr: Mapped["User"] = relationship(back_populates="vacancies")
    resumes: Mapped[list["Resume"]] = relationship(back_populates="vacancy")