# crud/emotion_entry.py
from sqlalchemy.orm import Session
from typing import List, Optional

import models.emotion_entry as emotion_model
import schemas.emotion_entry as emotion_schema

def get_emotion_entries(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[emotion_model.EmotionEntry]:
    """Retrieves a list of emotion entries for a specific user."""
    return db.query(emotion_model.EmotionEntry).filter(emotion_model.EmotionEntry.owner_id == user_id).offset(skip).limit(limit).all()

def get_emotion_entry(db: Session, emotion_entry_id: int) -> Optional[emotion_model.EmotionEntry]:
    """Retrieves a single emotion entry by its ID."""
    return db.query(emotion_model.EmotionEntry).filter(emotion_model.EmotionEntry.id == emotion_entry_id).first()

def create_user_emotion_entry(db: Session, emotion_entry: emotion_schema.EmotionEntryCreate, user_id: str) -> emotion_model.EmotionEntry:
    """Creates a new emotion entry for a specific user."""
    db_emotion_entry = emotion_model.EmotionEntry(**emotion_entry.model_dump(), owner_id=user_id)
    db.add(db_emotion_entry)
    db.commit()
    db.refresh(db_emotion_entry)
    return db_emotion_entry

def update_emotion_entry(db: Session, emotion_entry_id: int, emotion_update: emotion_schema.EmotionEntryUpdate) -> Optional[emotion_model.EmotionEntry]:
    """Updates an existing emotion entry. Handles partial updates."""
    db_emotion_entry = db.query(emotion_model.EmotionEntry).filter(emotion_model.EmotionEntry.id == emotion_entry_id).first()
    if db_emotion_entry:
        for key, value in emotion_update.model_dump(exclude_unset=True).items():
            setattr(db_emotion_entry, key, value)
        db.commit()
        db.refresh(db_emotion_entry)
    return db_emotion_entry

def delete_emotion_entry(db: Session, emotion_entry_id: int) -> Optional[emotion_model.EmotionEntry]:
    """Deletes an emotion entry by its ID."""
    db_emotion_entry = db.query(emotion_model.EmotionEntry).filter(emotion_model.EmotionEntry.id == emotion_entry_id).first()
    if db_emotion_entry:
        db.delete(db_emotion_entry)
        db.commit()
    return db_emotion_entry