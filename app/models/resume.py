from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, DateTime, func
from datetime import datetime, timezone
from typing import Optional
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False)
    higher_education: Mapped[bool] = mapped_column(Boolean, default=False)
    vacancy_id: Mapped[Optional[int]] = mapped_column(ForeignKey("vacancies.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now()
    )
    status: Mapped[str] = mapped_column(String(20), default="new", nullable=False)
    
    vacancy: Mapped[Optional["Vacancy"]] = relationship(back_populates="resumes")
    category: Mapped["Category"] = relationship(back_populates="resumes")