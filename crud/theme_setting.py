# crud/theme_setting.py
from sqlalchemy.orm import Session
from typing import Optional

import models.theme_setting as theme_model
import schemas.theme_setting as theme_schema

def get_theme_setting(db: Session, user_id: str) -> Optional[theme_model.ThemeSetting]:
    """Retrieves the theme setting for a specific user."""
    return db.query(theme_model.ThemeSetting).filter(theme_model.ThemeSetting.owner_id == user_id).first()

def create_or_update_user_theme_setting(db: Session, theme: theme_schema.ThemeSettingCreate, user_id: str) -> theme_model.ThemeSetting:
    """Creates or updates a theme setting for a user. Handles one-to-one relationship."""
    db_theme_setting = db.query(theme_model.ThemeSetting).filter(theme_model.ThemeSetting.owner_id == user_id).first()
    if db_theme_setting:
        for key, value in theme.model_dump().items():
            setattr(db_theme_setting, key, value)
    else:
        db_theme_setting = theme_model.ThemeSetting(**theme.model_dump(), owner_id=user_id)
        db.add(db_theme_setting)
    db.commit()
    db.refresh(db_theme_setting)
    return db_theme_setting