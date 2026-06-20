from typing import List
from uuid import UUID
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.database_connection import DatabaseConnection


class DatabaseConnectionRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(DatabaseConnection, db)

    def get_by_user_id(self, user_id: UUID) -> List[DatabaseConnection]:
        result = self.db.execute(
            select(DatabaseConnection).where(DatabaseConnection.user_id == user_id)
        )
        return list(result.scalars().all())
