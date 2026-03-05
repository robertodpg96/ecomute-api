from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
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

    bike: Mapped["Bike"] = relationship(back_populates="rentals")
    user: Mapped["User"] = relationship(back_populates="rentals")