# schemas/theme_setting.py
from pydantic import BaseModel, Field, validator
from typing import Optional
import re

# Base Schemas
class ThemeSettingBase(BaseModel):
    """Base schema for theme setting data."""
    primary_color: str
    font: str

    @validator('primary_color')
    def validate_color_format(cls, v):
        """Validates that primary_color is a valid hexadecimal color string."""
        if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', v):
            raise ValueError("Primary color must be a valid hexadecimal color string (e.g., #RRGGBB or #RGB).")
        return v

# Create Schemas
class ThemeSettingCreate(ThemeSettingBase):
    """Schema for creating or setting a theme."""
    pass

# Update Schemas
class ThemeSettingUpdate(ThemeSettingBase):
    """Schema for updating an existing theme setting (partial update allowed)."""
    primary_color: Optional[str] = None
    font: Optional[str] = None

    @validator('primary_color', pre=True, always=True)
    def validate_color_format_optional(cls, v):
        if v is not None:
            if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', v):
                raise ValueError("Primary color must be a valid hexadecimal color string (e.g., #RRGGBB or #RGB).")
        return v

# Response Schemas
class ThemeSettingResponse(ThemeSettingBase):
    """Schema for responding with theme setting data."""
    id: int
    owner_id: str

    class Config:
        from_attributes = True