from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime
from app.core.config import settings
from app.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup complete")
    yield
    print("Application shutdown complete")


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

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Internal server error", "error_code": "INTERNAL_SERVER_ERROR"}
        )

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "success": True,
            "data": {
                "status": "healthy",
                "version": settings.APP_VERSION,
                "timestamp": datetime.now().isoformat()
            },
            "message": "Service is healthy"
        }

    @app.get("/version", tags=["Health"])
    async def get_version():
        return {
            "success": True,
            "data": {
                "version": settings.APP_VERSION,
                "name": settings.APP_NAME,
                "environment": settings.ENVIRONMENT
            }
        }

    @app.get("/status", tags=["Health"])
    async def get_status():
        return {
            "success": True,
            "data": {
                "database": "connected (mock)",
                "redis": "connected (mock)",
                "overall": "healthy"
            }
        }

    # Include only the auth router temporarily
    from app.api.auth import router as auth_router
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])

    # Mock the other endpoints
    @app.get("/api/v1/history")
    async def mock_history():
        return {"success": True, "data": [], "total": 0, "page": 1, "page_size": 20}

    @app.get("/api/v1/saved-queries")
    async def mock_saved():
        return {"success": True, "data": [], "total": 0, "page": 1, "page_size": 20}

    @app.post("/api/v1/query")
    async def mock_query(request: Request):
        from pydantic import BaseModel

        class QueryRequest(BaseModel):
            question: str

        class QueryResult(BaseModel):
            query: str
            results: list[dict]
            columns: list[str]
            insight: str

        try:
            body = await request.json()
            question = body.get("question", "demo question")
            return {
                "success": True,
                "data": {
                    "query": "SELECT * FROM demo_table",
                    "results": [{"id": 1, "name": "Demo", "value": 100}],
                    "columns": ["id", "name", "value"],
                    "insight": f"Demo insight for your question: {question}"
                },
                "message": "Query executed successfully (mock)"
            }
        except Exception as e:
            return {"success": False, "error": str(e), "error_code": "MOCK_ERROR"}

    print(f"Application started: {settings.APP_NAME} v{settings.APP_VERSION}")
    return app


app = create_app()
