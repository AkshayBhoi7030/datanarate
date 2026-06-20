from typing import Optional
from uuid import UUID
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.organization import Organization


class OrganizationRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(Organization, db)

    def get_by_slug(self, slug: str) -> Optional[Organization]:
        return self.db.execute(select(Organization).where(Organization.slug == slug)).scalar_one_or_none()
