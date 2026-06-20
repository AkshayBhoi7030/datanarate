import re
from typing import Set
from app.core.exceptions import UnsafeSQLException
from app.core.logging import logger
from app.validators.sql_syntax_validator import SQLSyntaxValidator


class SQLValidator:
    BLOCKED_KEYWORDS: Set[str] = {
        "DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE", "INSERT",
        "CREATE", "GRANT", "REVOKE", "EXEC", "EXECUTE"
    }

    ALLOWED_KEYWORDS: Set[str] = {"SELECT", "WITH"}

    def validate(self, sql: str) -> bool:
        sql_upper = sql.strip().upper()
        first_word = sql_upper.split()[0] if sql_upper.split() else ""

        if first_word not in self.ALLOWED_KEYWORDS:
            logger.warning(f"Blocked SQL query - invalid start: {first_word}")
            raise UnsafeSQLException(f"Query must start with {', '.join(self.ALLOWED_KEYWORDS)}")

        for keyword in self.BLOCKED_KEYWORDS:
            # Use word boundaries to avoid false positives
            if re.search(rf"\b{keyword}\b", sql_upper):
                logger.warning(f"Blocked SQL query - contains forbidden keyword: {keyword}")
                raise UnsafeSQLException(f"Query contains forbidden keyword: {keyword}")

        # Validate SQL syntax
        is_valid, error_msg = SQLSyntaxValidator.validate_syntax(sql)
        if not is_valid:
            logger.warning(f"SQL syntax validation failed: {error_msg}")
            raise UnsafeSQLException(f"SQL syntax error: {error_msg}")

        logger.debug("SQL query passed security and syntax validation")
        return True
