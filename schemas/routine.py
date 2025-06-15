# schemas/routine.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import List, Optional

# Base Schemas
class RoutineBase(BaseModel):
    """Base schema for routine data."""
    title: str = Field(..., min_length=2, description="Routine title must be at least 2 characters.")
    days: List[str] = Field(..., min_items=1, description="Days must be a non-empty list of strings (e.g., ['Monday', 'Wednesday']).")
    deadline: date
    is_complete: bool = False

# Create Schemas
class RoutineCreate(RoutineBase):
    """Schema for creating a new routine."""
    pass

# Update Schemas
class RoutineUpdate(BaseModel):
    """Schema for updating an existing routine (partial update allowed)."""
    title: Optional[str] = Field(None, min_length=2)
    days: Optional[List[str]] = Field(None, min_items=1)
    deadline: Optional[date] = None
    is_complete: Optional[bool] = None

# Response Schemas
class RoutineResponse(RoutineBase):
    """Schema for responding with routine data."""
    id: int
    created_at: datetime
    owner_id: str

    class Config:
        from_attributes = True