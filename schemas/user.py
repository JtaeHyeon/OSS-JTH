# schemas/user.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base Schemas
class UserBase(BaseModel):
    """Base schema for user data."""
    username: str
    nickname: str

# Create Schemas
class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long.")
    nickname: Optional[str] = None # Override to make optional for creation

# Response Schemas
class UserResponse(UserBase):
    """Schema for responding with user data."""
    id: str
    
    created_at: datetime

    class Config:
        from_attributes = True