from typing import List
from uuid import UUID
from sqlalchemy import select, desc
from app.repositories.base import BaseRepository
from app.models.saved_query import SavedQuery


class SavedQueryRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(SavedQuery, db)

    def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[SavedQuery]:
        result = self.db.execute(
            select(SavedQuery)
            .where(SavedQuery.user_id == user_id)
            .order_by(desc(SavedQuery.created_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
