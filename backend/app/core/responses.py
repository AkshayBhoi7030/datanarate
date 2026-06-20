from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None
    error_code: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str


class StatusResponse(BaseModel):
    database: str
    redis: str
    overall: str
