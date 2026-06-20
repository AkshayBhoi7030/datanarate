from sqlalchemy.orm import Session
from app.core.logging import logger


class SchemaService:
    def __init__(self, db: Session):
        self.db = db

    def get_schema(self, connection_id):
        logger.debug(f"Fetching schema for connection: {connection_id}")
        return None
