from sqlalchemy import Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from datetime import datetime

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    priority: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('category.id'),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )