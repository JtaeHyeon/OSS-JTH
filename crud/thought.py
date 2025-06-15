# crud/thought.py
from sqlalchemy.orm import Session
from typing import List, Optional

import models.thought as thought_model
import schemas.thought as thought_schema

def get_thoughts(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[thought_model.Thought]:
    """Retrieves a list of thoughts for a specific user."""
    return db.query(thought_model.Thought).filter(thought_model.Thought.owner_id == user_id).offset(skip).limit(limit).all()

def get_thought(db: Session, thought_id: int) -> Optional[thought_model.Thought]:
    """Retrieves a single thought by its ID."""
    return db.query(thought_model.Thought).filter(thought_model.Thought.id == thought_id).first()

def create_user_thought(db: Session, thought: thought_schema.ThoughtCreate, user_id: str) -> thought_model.Thought:
    """Creates a new thought for a specific user."""
    db_thought = thought_model.Thought(**thought.model_dump(), owner_id=user_id)
    db.add(db_thought)
    db.commit()
    db.refresh(db_thought)
    return db_thought

def update_thought(db: Session, thought_id: int, thought_update: thought_schema.ThoughtUpdate) -> Optional[thought_model.Thought]:
    """Updates an existing thought. Supports updating content or edited_content."""
    db_thought = db.query(thought_model.Thought).filter(thought_model.Thought.id == thought_id).first()
    if db_thought:
        if thought_update.content is not None:
            db_thought.content = thought_update.content
        if thought_update.edited_content is not None:
            db_thought.edited_content = thought_update.edited_content
        db.commit()
        db.refresh(db_thought)
    return db_thought

def delete_thought(db: Session, thought_id: int) -> Optional[thought_model.Thought]:
    """Deletes a thought by its ID."""
    db_thought = db.query(thought_model.Thought).filter(thought_model.Thought.id == thought_id).first()
    if db_thought:
        db.delete(db_thought)
        db.commit()
    return db_thought