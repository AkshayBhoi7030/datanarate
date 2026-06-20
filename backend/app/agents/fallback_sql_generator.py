"""
Fallback SQL Generator - Rule-based SQL generation when Ollama is not available.
This provides basic SQL generation for common query patterns.
"""
import re
from typing import Optional, Dict, List, Tuple
from app.core.logging import logger
from app.rag.schema_introspection import SchemaIntrospectionService


class FallbackSQLGenerator:
    """Rule-based SQL generator for common queries when LLM is unavailable."""
    
    def __init__(self):
        self.schema_service = SchemaIntrospectionService()
        self.schema_cache = None
        
    def _get_schema(self) -> List[Dict]:
        """Get database schema as list of table dictionaries."""
        if self.schema_cache is None:
            tables = self.schema_service.get_schema()
            self.schema_cache = []
            for table in tables:
                table_dict = {
                    'name': table.name,
                    'columns': [col.name for col in table.columns],
                    'column_details': {col.name: str(col.data_type) for col in table.columns}
                }
                self.schema_cache.append(table_dict)
        return self.schema_cache
    
    def _find_table(self, keyword: str) -> Optional[Dict]:
        """Find table matching a keyword."""
        schema = self._get_schema()
        keyword_lower = keyword.lower()
        
        for table in schema:
            # Exact match
            if table['name'].lower() == keyword_lower:
                return table
            # Contains match
            if keyword_lower in table['name'].lower():
                return table
            # Plural/singular handling
            if keyword_lower.rstrip('s') == table['name'].lower().rstrip('s'):
                return table
        return None
    
    def _extract_limit(self, question: str) -> int:
        """Extract limit number from question."""
        # Look for patterns like "top 5", "first 10", etc.
        patterns = [
            r'(?:top|first)\s+(\d+)',
            r'limit\s+(\d+)',
            r'show\s+(\d+)',
            r'(\d+)\s+(?:records?|rows?|items?)',
        ]
        for pattern in patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                return int(match.group(1))
        return 100  # Default limit
    
    def _extract_order_column(self, question: str) -> Optional[str]:
        """Extract column to order by from question."""
        patterns = [
            r'(?:order|sort)\s+by\s+(\w+)',
            r'(?:by|order)\s+(\w+)\s+(?:asc|desc)',
            r'(\w+)\s+(?:highest|lowest|most|least)',
        ]
        for pattern in patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def generate_sql(self, question: str) -> Optional[str]:
        """
        Generate SQL query from natural language question using rule-based approach.
        Returns SQL string or None if question cannot be handled.
        """
        question_lower = question.lower()
        
        # Handle "Show all X" queries
        all_patterns = [
            r'show\s+all\s+(\w+)',
            r'list\s+all\s+(\w+)',
            r'get\s+all\s+(\w+)',
        ]
        for pattern in all_patterns:
            match = re.search(pattern, question_lower)
            if match:
                table_name = match.group(1)
                table = self._find_table(table_name)
                if table:
                    sql = f"SELECT * FROM {table['name']} LIMIT 100;"
                    logger.info(f"Fallback SQL (show all): {sql}")
                    return sql
        
        # Handle "Show X from table" queries
        column_patterns = [
            r'(?:show|get|list)\s+(\w+(?:\s*,\s*\w+)*)\s+from\s+(\w+)',
        ]
        for pattern in column_patterns:
            match = re.search(pattern, question_lower)
            if match:
                columns = match.group(1).replace(' ', '')
                table_name = match.group(2)
                table = self._find_table(table_name)
                if table:
                    sql = f"SELECT {columns} FROM {table['name']} LIMIT 100;"
                    logger.info(f"Fallback SQL (specific columns): {sql}")
                    return sql
        
        # Handle "Count" queries
        count_patterns = [
            r'(?:how\s+many|count)\s+(\w+)',
        ]
        for pattern in count_patterns:
            match = re.search(pattern, question_lower)
            if match:
                table_name = match.group(1)
                table = self._find_table(table_name)
                if table:
                    sql = f"SELECT COUNT(*) as count FROM {table['name']};"
                    logger.info(f"Fallback SQL (count): {sql}")
                    return sql
        
        # Handle "Top N by" queries (simple version)
        top_patterns = [
            r'(?:top|first)\s+(\d+)\s+(\w+)\s+(?:by|with|having)\s+(\w+)',
        ]
        for pattern in top_patterns:
            match = re.search(pattern, question_lower)
            if match:
                limit = int(match.group(1))
                table_name = match.group(2)
                order_col = match.group(3)
                table = self._find_table(table_name)
                if table:
                    sql = f"SELECT * FROM {table['name']} ORDER BY {order_col} DESC LIMIT {limit};"
                    logger.info(f"Fallback SQL (top N): {sql}")
                    return sql
        
        # If no pattern matched
        logger.warning(f"Fallback SQL generator could not handle question: {question}")
        return None
