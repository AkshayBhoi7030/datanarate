from fastapi import APIRouter
from app.api import auth, query, history, saved_queries, exports, preferences, audit_logs, websockets, schema, dashboard

router = APIRouter()
router.include_router(auth.router)
router.include_router(query.router)
router.include_router(history.router)
router.include_router(saved_queries.router)
router.include_router(exports.router)
router.include_router(preferences.router)
router.include_router(audit_logs.router)
router.include_router(websockets.router)
router.include_router(schema.router)
router.include_router(dashboard.router)
