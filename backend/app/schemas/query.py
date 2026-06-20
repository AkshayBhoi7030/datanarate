from pydantic import BaseModel
from typing import List, Dict, Any


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    sql: str
    data: List[Dict[str, Any]]
    insight: str
