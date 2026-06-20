from typing import List
from uuid import UUID
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.user_preferences import UserPreferences


class UserPreferencesRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(UserPreferences, db)

    def get_by_user_id(self, user_id: UUID):
        result = self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalars().first()
