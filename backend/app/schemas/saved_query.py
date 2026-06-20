from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class SavedQueryBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    natural_language_query: str
    generated_sql: str
    tags: Optional[List[str]] = None
    is_favorite: bool = False


class SavedQueryCreate(SavedQueryBase):
    pass


class SavedQueryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None


class SavedQueryResponse(SavedQueryBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
