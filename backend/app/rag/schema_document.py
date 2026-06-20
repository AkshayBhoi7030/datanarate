from typing import List
from app.rag.schema_introspection import TableSchema, ColumnSchema, RelationshipSchema


def table_to_document(table: TableSchema) -> str:
    lines = [f"Table: {table.name}"]
    lines.append("Columns:")
    for col in table.columns:
        pk_str = " (PK)" if col.is_primary_key else ""
        null_str = " NULL" if col.nullable else " NOT NULL"
        lines.append(f"  - {col.name} ({col.data_type}){pk_str}{null_str}")

    if table.relationships:
        lines.append("Relationships:")
        for rel in table.relationships:
            lines.append(f"  - {rel.source_table}.{rel.source_column} → {rel.target_table}.{rel.target_column}")

    return "\n".join(lines)


def schema_to_documents(tables: List[TableSchema]) -> List[dict]:
    documents = []
    for table in tables:
        doc = {
            "id": table.name,
            "text": table_to_document(table),
            "metadata": {
                "table_name": table.name,
                "column_count": len(table.columns),
                "relationship_count": len(table.relationships)
            }
        }
        documents.append(doc)
    return documents
