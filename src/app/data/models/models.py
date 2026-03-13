from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.data.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default='rider')
    is_active: Mapped[bool] = mapped_column(default=True)

    rentals: Mapped[List["Rental"]] = relationship(back_populates="user")

class Bike(Base):
    __tablename__ = "bikes"

    id: Mapped[int] = mapped_column(primary_key=True)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    battery: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    rentals: Mapped[List["Rental"]] = relationship(back_populates="bike")

class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    bike_id: Mapped[Optional[int]] = mapped_column(ForeignKey("bikes.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    bike: Mapped["Bike"] = relationship(back_populates="rentals")
    user: Mapped["User"] = relationship(back_populates="rentals")
