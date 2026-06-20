from typing import List
from uuid import UUID
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.query_history import QueryHistory


class QueryHistoryRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(QueryHistory, db)

    def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[QueryHistory]:
        result = self.db.execute(
            select(QueryHistory)
            .where(QueryHistory.user_id == user_id)
            .order_by(desc(QueryHistory.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
