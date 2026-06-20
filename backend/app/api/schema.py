
from fastapi import APIRouter
from app.rag.schema_introspection import SchemaIntrospectionService
from app.core.responses import APIResponse
from app.core.logging import logger
from pydantic import BaseModel
from typing import List, Optional


class ColumnSchemaResponse(BaseModel):
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = True


class TableSchemaResponse(BaseModel):
    table_name: str
    columns: List[ColumnSchemaResponse]


router = APIRouter(prefix="/schema", tags=["schema"])


@router.get("", response_model=APIResponse[List[TableSchemaResponse]])
def get_schema():
    introspector = SchemaIntrospectionService()
    schema = introspector.get_schema()
    
    response_data = []
    for table in schema:
        columns = []
        for col in table.columns:
            columns.append(ColumnSchemaResponse(
                name=col.name,
                type=str(col.data_type),
                primary_key=col.is_primary_key,
                nullable=col.nullable
            ))
        response_data.append(TableSchemaResponse(
            table_name=table.name,
            columns=columns
        ))
    
    return APIResponse(data=response_data)

