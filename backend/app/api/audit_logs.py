from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.repositories.audit_log import AuditLogRepository
from app.schemas.audit_log import AuditLogCreate, AuditLogResponse
from app.core.responses import APIResponse

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])

# Mock user ID
MOCK_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


@router.get("", response_model=APIResponse[list[AuditLogResponse]])
def get_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = AuditLogRepository(db)
    logs = repo.get_by_user_id(MOCK_USER_ID, skip, limit)
    return APIResponse(data=[AuditLogResponse.model_validate(log) for log in logs])


@router.post("", response_model=APIResponse[AuditLogResponse])
def create_audit_log(request: AuditLogCreate, db: Session = Depends(get_db)):
    repo = AuditLogRepository(db)
    log = repo.create(request.model_dump())
    return APIResponse(data=AuditLogResponse.model_validate(log))
