from __future__ import annotations
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base

class ThemeSetting(Base):
    __tablename__ = "theme_settings"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    primary_color: Mapped[str] = mapped_column(String)
    font: Mapped[str] = mapped_column(String)

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), unique=True)
    owner: Mapped["User"] = relationship("User", back_populates="theme_setting", foreign_keys=[user_id])

    def apply(self) -> None:
        print(f"Applying theme: Primary Color = {self.primary_color}, Font = {self.font}")

    def __repr__(self) -> str:
        return f"<ThemeSetting(id={self.id}, color='{self.primary_color}', font='{self.font}')>"