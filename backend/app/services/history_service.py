from sqlalchemy.orm import Session
from app.repositories.saved_query import SavedQueryRepository
from app.core.logging import logger


class HistoryService:
    def __init__(self, db: Session):
        self.db = db
        self.saved_query_repo = SavedQueryRepository(db)

    def get_saved_queries(self, user_id, skip=0, limit=100):
        logger.debug(f"Fetching saved queries for user: {user_id}")
        return self.saved_query_repo.get_by_user_id(user_id, skip, limit)
