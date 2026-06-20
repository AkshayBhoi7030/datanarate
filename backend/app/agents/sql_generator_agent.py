from typing import Optional
from app.llm.openrouter_service import OpenRouterService
from app.llm.ollama_service import OllamaService
from app.rag.rag_retriever import RAGRetriever
from app.agents.fallback_sql_generator import FallbackSQLGenerator
from app.prompts.sql_prompts import SQL_GENERATION_PROMPT
from app.core.logging import logger
from app.core.exceptions import DataNarrateException
import httpx


class SQLGeneratorAgent:
    def __init__(self):
        self.openrouter_service = OpenRouterService()
        self.ollama_service = OllamaService()
        self.rag_retriever = RAGRetriever()
        self.fallback_generator = FallbackSQLGenerator()
        self._openrouter_available = None
        self._ollama_available = None

    async def _check_openrouter_available(self) -> bool:
        """Check if OpenRouter is configured and available."""
        if self._openrouter_available is not None:
            return self._openrouter_available
        try:
            logger.debug("Checking OpenRouter availability...")
            is_available = await self.openrouter_service.check_connection()
            self._openrouter_available = is_available
            if is_available:
                logger.info("OpenRouter is available")
            else:
                logger.warning("OpenRouter is not available")
            return is_available
        except Exception as e:
            logger.error(f"Failed to check OpenRouter: {e}", exc_info=True)
        self._openrouter_available = False
        return False

    async def _check_ollama_available(self) -> bool:
        """Check if Ollama is running and available."""
        if self._ollama_available is not None:
            return self._ollama_available
        try:
            logger.debug("Checking Ollama availability...")
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get("http://localhost:11434/api/tags")
                if response.status_code == 200:
                    self._ollama_available = True
                    logger.info("Ollama is available")
                    return True
        except Exception as e:
            logger.error(f"Failed to check Ollama: {e}", exc_info=True)
        self._ollama_available = False
        return False

    async def generate_sql(self, question: str) -> str:
        logger.info(f"Generating SQL for question: {question}")

        # First, try fallback generator for simple patterns
        logger.debug("Trying fallback SQL generator...")
        fallback_sql = self.fallback_generator.generate_sql(question)
        if fallback_sql:
            logger.info(f"Using fallback SQL generator: {fallback_sql[:100]}...")
            return fallback_sql

        # Try OpenRouter first (primary)
        if await self._check_openrouter_available():
            try:
                logger.debug("Trying OpenRouter...")
                schema_context = self.rag_retriever.retrieve_relevant_schema(question)
                logger.debug(f"Retrieved schema context for OpenRouter: {schema_context[:100]}...")
                prompt = SQL_GENERATION_PROMPT.format(
                    schema_context=schema_context,
                    question=question
                )
                logger.debug("Sending request to OpenRouter...")
                sql = await self.openrouter_service.generate(
                    prompt=prompt,
                    temperature=0.1,
                    max_tokens=512
                )
                sql = self._clean_sql(sql)
                logger.info(f"Generated SQL via OpenRouter: {sql}")
                return sql
            except Exception as e:
                logger.error(f"OpenRouter generation failed: {e}", exc_info=True)
                # Fall through to Ollama or error

        # Try Ollama as fallback
        if await self._check_ollama_available():
            try:
                logger.debug("Trying Ollama...")
                schema_context = self.rag_retriever.retrieve_relevant_schema(question)
                logger.debug(f"Retrieved schema context for Ollama: {schema_context[:100]}...")
                prompt = SQL_GENERATION_PROMPT.format(
                    schema_context=schema_context,
                    question=question
                )
                logger.debug("Sending request to Ollama...")
                sql = await self.ollama_service.generate(
                    prompt=prompt,
                    temperature=0.1,
                    max_tokens=512
                )
                sql = self._clean_sql(sql)
                logger.info(f"Generated SQL via Ollama: {sql}")
                return sql
            except Exception as e:
                logger.error(f"Ollama generation failed: {e}", exc_info=True)
                raise DataNarrateException(
                    status_code=500,
                    detail=f"Failed to generate SQL. Ollama error: {str(e)}",
                    error_code="SQL_GENERATION_FAILED"
                )

        # Neither OpenRouter nor Ollama available, and fallback didn't match
        logger.error("No LLM service available")
        raise DataNarrateException(
            status_code=503,
            detail="No LLM service available. Please configure OpenRouter API key in settings or install Ollama for complex queries. You can also try simpler questions like 'show all products' or 'count customers'",
            error_code="LLM_UNAVAILABLE"
        )

    def _clean_sql(self, sql: str) -> str:
        # Remove any markdown fences and extra whitespace
        logger.debug(f"Cleaning SQL: {sql}")
        cleaned = sql.strip()
        if cleaned.startswith("```sql"):
            cleaned = cleaned[6:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        logger.debug(f"Cleaned SQL: {cleaned}")
        return cleaned
