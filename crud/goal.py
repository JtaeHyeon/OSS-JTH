# crud/goal.py
from sqlalchemy.orm import Session
from typing import List, Optional

import models.goal as goal_model
import schemas.goal as goal_schema
import schemas as schemas

def get_goals(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[goal_model.Goal]:
    """Retrieves a list of goals for a specific user."""
    return db.query(goal_model.Goal).filter(goal_model.Goal.owner_id == user_id).offset(skip).limit(limit).all()

def get_goal(db: Session, goal_id: int) -> Optional[goal_model.Goal]:
    """Retrieves a single goal by its ID."""
    return db.query(goal_model.Goal).filter(goal_model.Goal.id == goal_id).first()

def create_user_goal(db: Session, goal: goal_schema.GoalCreate, user_id: str) -> goal_model.Goal:
    """Creates a new goal for a specific user."""
    db_goal = goal_model.Goal(**goal.model_dump(), owner_id=user_id)
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

def update_goal(db: Session, goal_id: int, goal_update: schemas.goal.GoalUpdate) -> Optional[goal_model.Goal]:
    """Updates an existing goal. Handles partial updates."""
    db_goal = db.query(goal_model.Goal).filter(goal_model.Goal.id == goal_id).first()
    if db_goal:
        for key, value in goal_update.model_dump(exclude_unset=True).items():
            setattr(db_goal, key, value)
        db.commit()
        db.refresh(db_goal)
    return db_goal

def delete_goal(db: Session, goal_id: int) -> Optional[goal_model.Goal]:
    """Deletes a goal by its ID."""
    db_goal = db.query(goal_model.Goal).filter(goal_model.Goal.id == goal_id).first()
    if db_goal:
        db.delete(db_goal)
        db.commit()
    return db_goal