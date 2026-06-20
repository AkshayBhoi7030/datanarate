from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.repositories.query_history import QueryHistoryRepository
from app.schemas.query_history import QueryHistoryCreate, QueryHistoryResponse
from app.core.responses import APIResponse
from app.core.logging import logger

router = APIRouter(prefix="/history", tags=["history"])

# For now, we'll use mock IDs
MOCK_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
MOCK_ORG_ID = UUID("550e8400-e29b-41d4-a716-446655440002")


@router.get("", response_model=APIResponse[list[QueryHistoryResponse]])
def get_query_history(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    logger.info(f"Getting query history (skip={skip}, limit={limit})")
    try:
        repo = QueryHistoryRepository(db)
        history = repo.get_by_user_id(MOCK_USER_ID, skip, limit)
        logger.info(f"Retrieved {len(history)} history items")
        return APIResponse(data=[QueryHistoryResponse.model_validate(h) for h in history])
    except Exception as e:
        logger.error(f"Failed to get query history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get query history: {str(e)}")


@router.post("", response_model=APIResponse[QueryHistoryResponse])
def create_query_history(
    request: QueryHistoryCreate, db: Session = Depends(get_db)
):
    logger.info(f"Creating query history item for: {request.natural_language_query[:50]}...")
    try:
        repo = QueryHistoryRepository(db)
        history_item = repo.create({
            **request.model_dump(),
            "user_id": MOCK_USER_ID,
            "organization_id": MOCK_ORG_ID
        })
        logger.info(f"Query history item created: {history_item.id}")
        return APIResponse(data=QueryHistoryResponse.model_validate(history_item))
    except Exception as e:
        logger.error(f"Failed to create query history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create query history: {str(e)}")


@router.delete("/{history_id}", response_model=APIResponse[dict])
def delete_query_history(
    history_id: UUID, db: Session = Depends(get_db)
):
    logger.info(f"Deleting query history item: {history_id}")
    try:
        repo = QueryHistoryRepository(db)
        repo.remove(history_id)
        logger.info(f"Query history item deleted: {history_id}")
        return APIResponse(data={"message": "History item deleted successfully"})
    except Exception as e:
        logger.error(f"Failed to delete query history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete query history: {str(e)}")
