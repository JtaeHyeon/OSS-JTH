# schemas/emotion_entry.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

from models.emotion_entry import EmotionType # Import EmotionType enum

# Base Schemas
class EmotionEntryBase(BaseModel):
    """Base schema for emotion entry data."""
    emotion_type: str = Field(..., description=f"Emotion type must be one of: {', '.join(EmotionType.ALL_TYPES)}")
    level: int = Field(..., ge=1, le=10, description="Emotion level must be an integer between 1 and 10.")
    note: Optional[str] = None

    @validator('emotion_type')
    def validate_emotion_type(cls, v):
        """Validates that emotion_type is one of the predefined types."""
        if v not in EmotionType.ALL_TYPES:
            raise ValueError(f"Invalid emotion type. Must be one of: {', '.join(EmotionType.ALL_TYPES)}")
        return v

# Create Schemas
class EmotionEntryCreate(EmotionEntryBase):
    """Schema for creating a new emotion entry."""
    pass

# Update Schemas
class EmotionEntryUpdate(EmotionEntryBase):
    """Schema for updating an existing emotion entry (partial update allowed)."""
    emotion_type: Optional[str] = Field(None, description=f"Emotion type must be one of: {', '.join(EmotionType.ALL_TYPES)}")
    level: Optional[int] = Field(None, ge=1, le=10)
    note: Optional[str] = None

    @validator('emotion_type', pre=True, always=True)
    def validate_emotion_type_optional(cls, v):
        if v is not None:
            if v not in EmotionType.ALL_TYPES:
                raise ValueError(f"Invalid emotion type. Must be one of: {', '.join(EmotionType.ALL_TYPES)}")
        return v

# Response Schemas
class EmotionEntryResponse(EmotionEntryBase):
    """Schema for responding with emotion entry data."""
    id: int
    date: datetime
    owner_id: str

    class Config:
        from_attributes = True