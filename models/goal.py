from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String)
    deadline = Column(Date, nullable=True)
    progress = Column(Float, default=0.0)

    def update_progress(self, p: float) -> None:
        if not (0.0 <= p <= 1.0):
            raise ValueError("진행률은 0.0 ~ 1.0 사이여야 합니다.")
        self.progress = p

    def __repr__(self) -> str:
        return f"<Goal(id={self.id}, nickname='{self.nickname}', title='{self.title}', progress={self.progress})>"
