from sqlalchemy.orm import Session
from app.repositories.query_history import QueryHistoryRepository
from app.core.logging import logger


class QueryService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = QueryHistoryRepository(db)

    def get_query_history(self, user_id, skip=0, limit=100):
        logger.debug(f"Fetching query history for user: {user_id}")
        return self.repository.get_by_user_id(user_id, skip, limit)
