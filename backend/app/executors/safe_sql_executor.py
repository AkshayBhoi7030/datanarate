from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.validators.sql_validator import SQLValidator
from app.core.logging import logger


class SafeSQLExecutor:
    def __init__(self):
        self.db_url = settings.DATABASE_URL
        self.engine = create_engine(self.db_url)
        self.validator = SQLValidator()

    def execute(self, sql: str) -> List[Dict[str, Any]]:
        logger.info(f"Executing SQL query: {sql}")

        try:
            logger.debug("Validating SQL...")
            self.validator.validate(sql)
            logger.debug("SQL validation passed")
        except Exception as e:
            logger.error(f"SQL validation failed: {e}", exc_info=True)
            raise

        try:
            logger.debug("Connecting to database...")
            with self.engine.connect() as conn:
                logger.debug("Executing query...")
                result = conn.execute(text(sql))
                columns = result.keys()
                logger.debug(f"Columns returned: {list(columns)}")
                rows = result.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                logger.info(f"SQL executed successfully, returned {len(data)} rows")
                logger.debug(f"Data sample: {data[:2] if data else 'empty'}")
                return data
        except Exception as e:
            logger.error(f"SQL execution failed: {e}", exc_info=True)
            raise
