# schemas/goal.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

# Base Schemas
class GoalBase(BaseModel):
    """Base schema for goal data."""
    title: str = Field(..., min_length=2, description="Goal title must be at least 2 characters.")
    content: str = Field(..., min_length=5, description="Goal content must be at least 5 characters.")
    deadline: date
    progress: float = Field(0.0, ge=0.0, le=1.0, description="Progress must be between 0.0 and 1.0.")

# Create Schemas
class GoalCreate(GoalBase):
    """Schema for creating a new goal."""
    pass

# Update Schemas
class GoalUpdate(BaseModel):
    """Schema for updating an existing goal (partial update allowed)."""
    title: Optional[str] = Field(None, min_length=2)
    content: Optional[str] = Field(None, min_length=5)
    deadline: Optional[date] = None
    progress: Optional[float] = Field(None, ge=0.0, le=1.0)

# Response Schemas
class GoalResponse(GoalBase):
    """Schema for responding with goal data."""
    id: int
    created_at: datetime
    owner_id: str

    class Config:
        from_attributes = True