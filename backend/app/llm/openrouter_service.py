"""
OpenRouter Service - Handles LLM API calls through OpenRouter.
"""
import httpx
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.core.logging import logger


class OpenRouterService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = settings.OPENROUTER_MODEL
        self.timeout = settings.OPENROUTER_TIMEOUT
        self.max_retries = settings.OPENROUTER_MAX_RETRIES
        
        if not self.api_key or self.api_key == "<OPENROUTER_API_KEY>":
            logger.warning("OpenRouter API key not configured")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def check_connection(self) -> bool:
        """Check if OpenRouter API is accessible."""
        try:
            if not self.api_key or self.api_key == "<OPENROUTER_API_KEY>":
                logger.error("OpenRouter API key not configured")
                return False
                
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    "https://openrouter.ai/api/v1/auth/key",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                if response.status_code == 200:
                    logger.info("Successfully connected to OpenRouter API")
                    return True
                else:
                    logger.warning(f"OpenRouter auth failed: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Failed to connect to OpenRouter: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.1,
        max_tokens: int = 512,
        top_p: float = 0.95,
    ) -> str:
        """Generate text using OpenRouter API."""
        try:
            if not self.api_key or self.api_key == "<OPENROUTER_API_KEY>":
                raise ValueError("OpenRouter API key not configured. Please set OPENROUTER_API_KEY in your .env file.")
                
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
            }

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract generated text from response
                if "choices" in result and len(result["choices"]) > 0:
                    generated_text = result["choices"][0].get("message", {}).get("content", "").strip()
                    logger.debug(f"OpenRouter generated response of length {len(generated_text)}")
                    return generated_text
                else:
                    logger.error(f"Unexpected response format: {result}")
                    raise ValueError("Unexpected response format from OpenRouter")

        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.TimeoutException as e:
            logger.error(f"OpenRouter timeout after {self.timeout}s")
            raise
        except Exception as e:
            logger.error(f"OpenRouter generation failed: {str(e)}")
            raise
