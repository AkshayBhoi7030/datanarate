import httpx
from typing import Optional, Dict, Any
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings
from app.core.logging import logger


class OllamaService:
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = settings.OLLAMA_MODEL
        self.timeout = settings.OLLAMA_TIMEOUT
        self.max_retries = settings.OLLAMA_MAX_RETRIES

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def check_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    logger.info(f"Successfully connected to Ollama at {self.base_url}")
                    models = response.json().get("models", [])
                    model_names = [m["name"] for m in models]
                    if self.model in model_names:
                        logger.info(f"Model {self.model} is available")
                        return True
                    else:
                        logger.warning(f"Model {self.model} not found in Ollama models: {model_names}")
                        return False
                return False
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {str(e)}")
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
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_p": top_p
                }
            }

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                generated_text = result.get("response", "").strip()
                logger.debug(f"Ollama generated response of length {len(generated_text)}")
                return generated_text

        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.TimeoutException as e:
            logger.error(f"Ollama timeout after {self.timeout}s")
            raise
        except Exception as e:
            logger.error(f"Ollama generation failed: {str(e)}")
            raise
