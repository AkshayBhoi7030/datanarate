import json
import hashlib
from typing import Optional, Any, List, Dict
from app.core.config import settings
from app.core.logging import logger


class RedisCache:
    def __init__(self):
        self.redis_client = None
        self._fallback_cache: Dict[str, Any] = {}  # In-memory fallback if Redis fails

    async def connect(self):
        try:
            import redis.asyncio as redis
            self.redis_client = redis.from_url(settings.REDIS_URL)
            await self.redis_client.ping()
            logger.info("Connected to Redis cache successfully")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis, using in-memory cache: {e}")
            self.redis_client = None

    async def disconnect(self):
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis cache")

    def _get_key(self, prefix: str, question: str) -> str:
        question_hash = hashlib.sha256(question.encode()).hexdigest()
        return f"{prefix}:{question_hash}"

    async def get_sql(self, question: str) -> Optional[str]:
        if self.redis_client:
            key = self._get_key("sql", question)
            cached = await self.redis_client.get(key)
            if cached:
                logger.debug(f"Cache hit (Redis) for SQL: {question[:50]}")
                return cached.decode("utf-8")
        else:
            key = self._get_key("sql", question)
            if key in self._fallback_cache:
                logger.debug(f"Cache hit (memory) for SQL: {question[:50]}")
                return self._fallback_cache[key]
        return None

    async def set_sql(self, question: str, sql: str, ttl: Optional[int] = None):
        if self.redis_client:
            key = self._get_key("sql", question)
            ttl = ttl or settings.CACHE_TTL_SQL
            await self.redis_client.setex(key, ttl, sql)
            logger.debug(f"Cached SQL (Redis) for: {question[:50]}")
        else:
            key = self._get_key("sql", question)
            self._fallback_cache[key] = sql
            logger.debug(f"Cached SQL (memory) for: {question[:50]}")

    async def get_results(self, question: str) -> Optional[List[Dict[str, Any]]]:
        if self.redis_client:
            key = self._get_key("results", question)
            cached = await self.redis_client.get(key)
            if cached:
                logger.debug(f"Cache hit (Redis) for results: {question[:50]}")
                return json.loads(cached)
        else:
            key = self._get_key("results", question)
            if key in self._fallback_cache:
                logger.debug(f"Cache hit (memory) for results: {question[:50]}")
                return self._fallback_cache[key]
        return None

    async def set_results(self, question: str, results: List[Dict[str, Any]], ttl: Optional[int] = None):
        if self.redis_client:
            key = self._get_key("results", question)
            ttl = ttl or settings.CACHE_TTL_RESULTS
            await self.redis_client.setex(key, ttl, json.dumps(results))
            logger.debug(f"Cached results (Redis) for: {question[:50]}")
        else:
            key = self._get_key("results", question)
            self._fallback_cache[key] = results
            logger.debug(f"Cached results (memory) for: {question[:50]}")

    async def get_insights(self, question: str) -> Optional[str]:
        if self.redis_client:
            key = self._get_key("insights", question)
            cached = await self.redis_client.get(key)
            if cached:
                logger.debug(f"Cache hit (Redis) for insights: {question[:50]}")
                return cached.decode("utf-8")
        else:
            key = self._get_key("insights", question)
            if key in self._fallback_cache:
                logger.debug(f"Cache hit (memory) for insights: {question[:50]}")
                return self._fallback_cache[key]
        return None

    async def set_insights(self, question: str, insights: str, ttl: Optional[int] = None):
        if self.redis_client:
            key = self._get_key("insights", question)
            ttl = ttl or settings.CACHE_TTL_INSIGHTS
            await self.redis_client.setex(key, ttl, insights)
            logger.debug(f"Cached insights (Redis) for: {question[:50]}")
        else:
            key = self._get_key("insights", question)
            self._fallback_cache[key] = insights
            logger.debug(f"Cached insights (memory) for: {question[:50]}")

    async def invalidate_question(self, question: str):
        if self.redis_client:
            for prefix in ["sql", "results", "insights"]:
                key = self._get_key(prefix, question)
                await self.redis_client.delete(key)
        else:
            for prefix in ["sql", "results", "insights"]:
                key = self._get_key(prefix, question)
                if key in self._fallback_cache:
                    del self._fallback_cache[key]
        logger.debug(f"Invalidated cache for: {question[:50]}")


# Singleton instance
redis_cache = RedisCache()
