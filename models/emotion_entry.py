from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class EmotionType:
    HAPPY = "Happy"
    SAD = "Sad"
    ANGRY = "Angry"
    NEUTRAL = "Neutral"
    EXCITED = "Excited"
    CALM = "Calm"
    ALL_TYPES = [HAPPY, SAD, ANGRY, NEUTRAL, EXCITED, CALM]

class EmotionEntry(Base):
    __tablename__ = "emotion_entries"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    emotion_type: Mapped[str] = mapped_column(String)
    level: Mapped[int] = mapped_column(Integer)
    note: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="emotions", foreign_keys=[user_id])

    def __repr__(self) -> str:
        return f"<EmotionEntry(id={self.id}, type='{self.emotion_type}', level={self.level})>"