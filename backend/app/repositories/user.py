from typing import Optional
from uuid import UUID
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.user import User


class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.execute(select(User).where(User.email == email)).scalar_one_or_none()
