from datetime import datetime, date
from typing import List, Optional
import hashlib
import uuid

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, Date, Enum, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Mapped, mapped_column
from sqlalchemy.types import TypeDecorator, String as StringType

DATABASE_URL = "sqlite:///./sql_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_db_tables():
    from . import user, routine, goal, emotion_entry, thought, theme_setting
    Base.metadata.create_all(bind=engine)
    print("Database tables created or already exist.")
