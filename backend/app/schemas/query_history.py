from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class QueryHistoryBase(BaseModel):
    natural_language_query: str
    generated_sql: str


class QueryHistoryCreate(QueryHistoryBase):
    database_connection_id: UUID
    execution_time_ms: Optional[int] = None
    row_count: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None


class QueryHistoryResponse(QueryHistoryBase):
    id: UUID
    user_id: UUID
    database_connection_id: UUID
    execution_time_ms: Optional[int] = None
    row_count: Optional[int] = None
    success: bool
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
