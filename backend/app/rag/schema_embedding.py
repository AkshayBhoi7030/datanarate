from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from app.core.config import settings
from app.core.logging import logger
from app.rag.schema_introspection import TableSchema
from app.rag.schema_document import schema_to_documents


class SchemaEmbeddingService:
    def __init__(self):
        self.persist_dir = settings.CHROMADB_PERSIST_DIR
        self.collection_name = settings.CHROMADB_COLLECTION
        self.client = chromadb.Client(Settings(
            persist_directory=self.persist_dir,
            is_persistent=True
        ))
        self.collection = self._get_or_create_collection()
        logger.info(f"SchemaEmbeddingService initialized with collection: {self.collection_name}")

    def _get_or_create_collection(self):
        try:
            coll = self.client.get_collection(self.collection_name)
            logger.debug(f"Retrieved existing collection: {self.collection_name}")
            return coll
        except Exception:
            coll = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "DataNarrate database schema embeddings"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
            return coll

    def embed_schema(self, tables: List[TableSchema]):
        documents = schema_to_documents(tables)
        ids = [doc["id"] for doc in documents]
        texts = [doc["text"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        self.collection.upsert(ids=ids, documents=texts, metadatas=metadatas)
        logger.info(f"Embedded {len(tables)} tables into collection")

    def update_schema(self, tables: List[TableSchema]):
        self.embed_schema(tables)

    def delete_table(self, table_name: str):
        try:
            self.collection.delete(ids=[table_name])
            logger.info(f"Deleted table {table_name} from embeddings")
        except Exception as e:
            logger.error(f"Error deleting table {table_name}: {e}")

    def search_schema(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        logger.debug(f"Schema search returned {len(results['documents'][0])} results for query: {query[:50]}")

        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        return formatted_results

    def get_all_tables(self) -> List[Dict[str, Any]]:
        result = self.collection.get()
        formatted = []
        for i in range(len(result["ids"])):
            formatted.append({
                "id": result["ids"][i],
                "text": result["documents"][i],
                "metadata": result["metadatas"][i]
            })
        return formatted

    def clear_collection(self):
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "DataNarrate database schema embeddings"}
        )
        logger.info(f"Cleared collection {self.collection_name}")
