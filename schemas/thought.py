# schemas/thought.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Base Schemas
class ThoughtBase(BaseModel):
    """Base schema for thought data."""
    content: str = Field(..., min_length=5, description="Thought content must be at least 5 characters.")

# Create Schemas
class ThoughtCreate(ThoughtBase):
    """Schema for creating a new thought."""
    pass

# Update Schemas
class ThoughtUpdate(BaseModel):
    """Schema for updating an existing thought (supports original content or edited content)."""
    content: Optional[str] = Field(None, min_length=5, description="New main content for the thought.")
    edited_content: Optional[str] = Field(None, min_length=5, description="Explicitly set the edited version of the thought.")

# Response Schemas
class ThoughtResponse(ThoughtBase):
    """Schema for responding with thought data."""
    id: int
    created_at: datetime
    edited_content: Optional[str]
    owner_id: str

    class Config:
        from_attributes = True