# schemas/daily_summary.py
from pydantic import BaseModel
from datetime import date

class DailySummaryResponse(BaseModel):
    """Schema for responding with daily summary data."""
    summary_date: date
    summary_string: str