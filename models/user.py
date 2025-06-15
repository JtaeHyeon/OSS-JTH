from __future__ import annotations
from datetime import datetime
from typing import List, Optional
import hashlib
import uuid

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    nickname: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    emotions: Mapped[List["EmotionEntry"]] = relationship("EmotionEntry", back_populates="owner", foreign_keys="EmotionEntry.user_id")
    routines: Mapped[List["Routine"]] = relationship("Routine", back_populates="owner", foreign_keys="Routine.user_id")
    goals: Mapped[List["Goal"]] = relationship("Goal", back_populates="owner", foreign_keys="Goal.user_id")
    thoughts: Mapped[List["Thought"]] = relationship("Thought", back_populates="owner", foreign_keys="Thought.user_id")
    theme_setting: Mapped[Optional["ThemeSetting"]] = relationship("ThemeSetting", back_populates="owner", uselist=False, foreign_keys="ThemeSetting.user_id")

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def set_password(self, plain_password: str) -> None:
        if not plain_password or not isinstance(plain_password, str) or len(plain_password) < 8:
            raise ValueError("Password must be a non-empty string of at least 8 characters.")
        self.hashed_password = self._hash_password(plain_password)

    def check_password(self, plain_password: str) -> bool:
        return self.hashed_password == self._hash_password(plain_password)

    def __repr__(self) -> str:
        return f"<User(id='{self.id}', username='{self.username}', nickname='{self.nickname}')>"
