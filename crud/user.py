# crud/user.py
from sqlalchemy.orm import Session
from typing import Optional

import models.user as user_model
import schemas.user as user_schema

def get_user(db: Session, user_id: str) -> Optional[user_model.User]:
    """Retrieves a user by their ID."""
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[user_model.User]:
    """Retrieves a user by their username."""
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def create_user(db: Session, user: user_schema.UserCreate) -> user_model.User:
    """Creates a new user and hashes their password."""
    db_user = user_model.User(username=user.username, nickname=user.nickname if user.nickname else user.username)
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    hashed_pw = hash_password(user.password)  # 비밀번호 해시
    db_user = models.User(username=user.username, nickname=user.nickname, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> Optional[user_model.User]:
    """Deletes a user by their ID. Cascade deletes related data."""
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user