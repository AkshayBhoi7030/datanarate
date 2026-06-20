from typing import Dict, List, Any
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Inspector
from app.core.config import settings
from app.core.logging import logger


class ColumnSchema:
    def __init__(
        self,
        name: str,
        data_type: str,
        nullable: bool,
        default: Any = None,
        is_primary_key: bool = False
    ):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.default = default
        self.is_primary_key = is_primary_key


class RelationshipSchema:
    def __init__(
        self,
        source_table: str,
        source_column: str,
        target_table: str,
        target_column: str
    ):
        self.source_table = source_table
        self.source_column = source_column
        self.target_table = target_table
        self.target_column = target_column


class TableSchema:
    def __init__(
        self,
        name: str,
        columns: List[ColumnSchema],
        relationships: List[RelationshipSchema] = None
    ):
        self.name = name
        self.columns = columns
        self.relationships = relationships or []


class SchemaIntrospectionService:
    def __init__(self, db_url: str = None):
        self.db_url = db_url or settings.DATABASE_URL
        self.engine = create_engine(self.db_url)

    def get_schema(self) -> List[TableSchema]:
        inspector = Inspector.from_engine(self.engine)
        all_tables = []

        for table_name in inspector.get_table_names():
            columns = []
            for col in inspector.get_columns(table_name):
                col_schema = ColumnSchema(
                    name=col["name"],
                    data_type=str(col["type"]),
                    nullable=col["nullable"],
                    default=col.get("default"),
                    is_primary_key=col.get("primary_key", False)
                )
                columns.append(col_schema)

            relationships = []
            for fk in inspector.get_foreign_keys(table_name):
                for col, ref in zip(fk["constrained_columns"], fk["referred_columns"]):
                    rel = RelationshipSchema(
                        source_table=table_name,
                        source_column=col,
                        target_table=fk["referred_table"],
                        target_column=ref
                    )
                    relationships.append(rel)

            table_schema = TableSchema(
                name=table_name,
                columns=columns,
                relationships=relationships
            )
            all_tables.append(table_schema)
            logger.debug(f"Introspected table: {table_name} with {len(columns)} columns")

        logger.info(f"Introspected {len(all_tables)} tables from database")
        return all_tables

    def get_table_schema(self, table_name: str) -> TableSchema:
        inspector = Inspector.from_engine(self.engine)
        columns = []
        for col in inspector.get_columns(table_name):
            col_schema = ColumnSchema(
                name=col["name"],
                data_type=str(col["type"]),
                nullable=col["nullable"],
                default=col.get("default"),
                is_primary_key=col.get("primary_key", False)
            )
            columns.append(col_schema)

        relationships = []
        for fk in inspector.get_foreign_keys(table_name):
            for col, ref in zip(fk["constrained_columns"], fk["referred_columns"]):
                rel = RelationshipSchema(
                    source_table=table_name,
                    source_column=col,
                    target_table=fk["referred_table"],
                    target_column=ref
                )
                relationships.append(rel)

        return TableSchema(
            name=table_name,
            columns=columns,
            relationships=relationships
        )
