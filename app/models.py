
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        nullable=False
    )

class Calculation(Base):
    __tablename__ = "calculations"

    id: Mapped[int] = mapped_column(primary_key=True)

    a: Mapped[float] = mapped_column(Float, nullable=False)
    b: Mapped[float] = mapped_column(Float, nullable=False)

    type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    result: Mapped[float] = mapped_column(Float, nullable=False)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
