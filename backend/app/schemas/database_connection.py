from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.database_connection import DatabaseType


class DatabaseConnectionBase(BaseModel):
    name: str = Field(..., max_length=255)
    db_type: DatabaseType
    host: str = Field(..., max_length=255)
    port: str = Field(..., max_length=10)
    database: str = Field(..., max_length=255)
    username: str = Field(..., max_length=255)
    description: Optional[str] = None


class DatabaseConnectionCreate(DatabaseConnectionBase):
    password: str = Field(..., max_length=255)


class DatabaseConnectionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    host: Optional[str] = Field(None, max_length=255)
    port: Optional[str] = Field(None, max_length=10)
    database: Optional[str] = Field(None, max_length=255)
    username: Optional[str] = Field(None, max_length=255)
    password: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class DatabaseConnectionResponse(DatabaseConnectionBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
