import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.logging import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        method = request.method
        url = str(request.url)

        logger.info(f"Request started: {method} {url}")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            response.headers["X-Process-Time"] = str(process_time)

            logger.info(
                f"Request completed: {method} {url} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.2f}ms"
            )

            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: {method} {url} - "
                f"Error: {str(e)} - "
                f"Time: {process_time:.2f}ms"
            )
            raise
