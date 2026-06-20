from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from uuid import UUID


class UserPreferencesBase(BaseModel):
    theme: str = "light"
    dashboard_settings: Dict = Field(default_factory=dict)
    saved_filters: List = Field(default_factory=list)
    preferred_chart_type: str = "bar"


class UserPreferencesUpdate(BaseModel):
    theme: Optional[str] = None
    dashboard_settings: Optional[Dict] = None
    saved_filters: Optional[List] = None
    preferred_chart_type: Optional[str] = None


class UserPreferencesResponse(UserPreferencesBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
