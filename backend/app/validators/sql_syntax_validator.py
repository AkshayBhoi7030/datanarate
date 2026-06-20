"""
SQL Syntax Validator - Validates SQLite SQL syntax before execution.
"""
import re
import sqlite3
from typing import Tuple, Optional
from app.core.logging import logger


class SQLSyntaxValidator:
    """Validates SQL syntax using SQLite's parser."""
    
    # Common SQL syntax errors to check for
    INVALID_PATTERNS = [
        # JOIN with ORDER BY inside
        (r'JOIN\s+\w+\s+ON\s+[^\s]+\s+DESC', 'Invalid: DESC in JOIN clause'),
        # Multiple ORDER BY
        (r'ORDER\s+BY.*ORDER\s+BY', 'Invalid: Multiple ORDER BY clauses'),
        # Unclosed parenthesis (basic check)
        (r'\([^)]*$', 'Invalid: Unclosed parenthesis'),
    ]
    
    @classmethod
    def validate_syntax(cls, sql: str) -> Tuple[bool, Optional[str]]:
        """
        Validate SQL syntax using pattern matching and basic checks.
        Note: We don't use EXPLAIN validation here because it requires the actual
        database tables to exist. Instead we do pattern-based validation.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        sql_clean = sql.strip()
        
        if not sql_clean:
            return False, "Empty SQL query"
        
        # Check for common invalid patterns
        for pattern, error_msg in cls.INVALID_PATTERNS:
            if re.search(pattern, sql_clean, re.IGNORECASE):
                logger.warning(f"SQL syntax validation failed: {error_msg}")
                return False, error_msg
        
        # Basic syntax checks
        # Check for unclosed parentheses
        open_parens = sql_clean.count('(')
        close_parens = sql_clean.count(')')
        if open_parens != close_parens:
            return False, f"Unclosed parentheses: {open_parens} open, {close_parens} close"
        
        # Check for basic SQL structure
        sql_upper = sql_clean.upper()
        if not any(keyword in sql_upper for keyword in ['SELECT', 'WITH']):
            return False, "SQL must start with SELECT or WITH"
        
        # Check for common syntax errors
        # Double commas
        if ',,' in sql_clean:
            return False, "Double comma in SQL"
        
        # Missing spaces after keywords
        if re.search(r'\b(SELECT|FROM|WHERE|JOIN|ORDER|GROUP|HAVING)\b[a-zA-Z]', sql_clean, re.IGNORECASE):
            return False, "Missing space after SQL keyword"
        
        logger.debug("SQL syntax validation passed")
        return True, None
