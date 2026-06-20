from typing import List
from uuid import UUID
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.audit_log import AuditLog


class AuditLogRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(AuditLog, db)

    def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        result = self.db.execute(
            select(AuditLog)
            .where(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
