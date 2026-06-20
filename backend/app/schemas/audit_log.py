from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models.audit_log import AuditAction


class AuditLogBase(BaseModel):
    action: AuditAction
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    user_id: Optional[UUID] = None


class AuditLogResponse(AuditLogBase):
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime

    model_config = {"from_attributes": True}
