from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, UTC
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import DataNarrateException
from app.core.responses import APIResponse, HealthResponse, StatusResponse
from app.core.cache import redis_cache
from app.middleware.logging import LoggingMiddleware
from app.db.session import engine
from app.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_cache.connect()
    logger.info("Application startup complete")
    yield
    await redis_cache.disconnect()
    logger.info("Application shutdown complete")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)

    @app.exception_handler(DataNarrateException)
    async def datanarrate_exception_handler(request: Request, exc: DataNarrateException):
        logger.error(f"Exception: {exc.error_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=APIResponse(
                success=False,
                error=str(exc.detail),
                error_code=exc.error_code,
            ).model_dump()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content=APIResponse(
                success=False,
                error="Internal server error",
                error_code="INTERNAL_SERVER_ERROR",
            ).model_dump()
        )

    @app.get("/health", response_model=APIResponse[HealthResponse], tags=["Health"])
    async def health_check():
        return APIResponse(
            data=HealthResponse(
                status="healthy",
                version=settings.APP_VERSION,
                timestamp=datetime.now(UTC).isoformat().replace("+00:00", "Z")
            ),
            message="Service is healthy"
        )

    @app.get("/version", response_model=APIResponse[dict], tags=["Health"])
    async def get_version():
        return APIResponse(
            data={
                "version": settings.APP_VERSION,
                "name": settings.APP_NAME,
                "environment": settings.ENVIRONMENT
            }
        )

    @app.get("/status", response_model=APIResponse[StatusResponse], tags=["Health"])
    async def get_status():
        db_status = "healthy"
        redis_status = "healthy"

        try:
            with engine.connect() as conn:
                from sqlalchemy import text
                conn.execute(text("SELECT 1"))
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            db_status = "unhealthy"

        try:
            import redis.asyncio as redis
            r = redis.from_url(settings.REDIS_URL)
            await r.ping()
            await r.close()
        except Exception as e:
            logger.error(f"Redis connection failed: {str(e)}")
            redis_status = "unhealthy"

        overall = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"

        return APIResponse(
            data=StatusResponse(
                database=db_status,
                redis=redis_status,
                overall=overall
            )
        )

    app.include_router(api_router, prefix="/api/v1")

    logger.info(f"Application started: {settings.APP_NAME} v{settings.APP_VERSION}")
    return app


app = create_app()
