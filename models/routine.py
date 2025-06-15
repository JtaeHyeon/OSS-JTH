from __future__ import annotations
from datetime import datetime, date
from typing import List

from sqlalchemy import Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from models.custom_types import ListOfString

class Routine(Base):
    __tablename__ = "routines"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)
    days: Mapped[List[str]] = mapped_column(ListOfString)
    deadline: Mapped[date] = mapped_column(Date)
    is_complete: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))

    owner: Mapped["User"] = relationship("User", back_populates="routines", foreign_keys=[user_id])

    def toggle_complete(self) -> None:
        self.is_complete = not self.is_complete

    def __repr__(self) -> str:
        return f"<Routine(id={self.id}, title='{self.title}', is_complete={self.is_complete})>"
