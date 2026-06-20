from typing import List, Dict, Any
from app.rag.schema_embedding import SchemaEmbeddingService
from app.core.logging import logger


class RAGRetriever:
    def __init__(self):
        self.embedding_service = SchemaEmbeddingService()

    def retrieve_relevant_schema(self, question: str, n_results: int = 5) -> str:
        results = self.embedding_service.search_schema(question, n_results)
        context_parts = []
        for res in results:
            context_parts.append(res["text"])
        context = "\n\n".join(context_parts)
        logger.info(f"Retrieved {len(results)} relevant schema parts for question")
        return context
