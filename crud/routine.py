# crud/routine.py
from sqlalchemy.orm import Session
from typing import List, Optional

import models.routine as routine_model
import schemas.routine as routine_schema

def get_routines(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[routine_model.Routine]:
    """Retrieves a list of routines for a specific user."""
    return db.query(routine_model.Routine).filter(routine_model.Routine.owner_id == user_id).offset(skip).limit(limit).all()

def get_routine(db: Session, routine_id: int) -> Optional[routine_model.Routine]:
    """Retrieves a single routine by its ID."""
    return db.query(routine_model.Routine).filter(routine_model.Routine.id == routine_id).first()

def create_user_routine(db: Session, routine: routine_schema.RoutineCreate, user_id: str) -> routine_model.Routine:
    """Creates a new routine for a specific user."""
    db_routine = routine_model.Routine(**routine.model_dump(), owner_id=user_id)
    db.add(db_routine)
    db.commit()
    db.refresh(db_routine)
    return db_routine

def update_routine(db: Session, routine_id: int, routine_update: routine_schema.RoutineUpdate) -> Optional[routine_model.Routine]:
    """Updates an existing routine. Handles partial updates."""
    db_routine = db.query(routine_model.Routine).filter(routine_model.Routine.id == routine_id).first()
    if db_routine:
        for key, value in routine_update.model_dump(exclude_unset=True).items():
            setattr(db_routine, key, value)
        db.commit()
        db.refresh(db_routine)
    return db_routine

def delete_routine(db: Session, routine_id: int) -> Optional[routine_model.Routine]:
    """Deletes a routine by its ID."""
    db_routine = db.query(routine_model.Routine).filter(routine_model.Routine.id == routine_id).first()
    if db_routine:
        db.delete(db_routine)
        db.commit()
    return db_routine