from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.repositories.saved_query import SavedQueryRepository
from app.schemas.saved_query import SavedQueryCreate, SavedQueryUpdate, SavedQueryResponse
from app.core.responses import APIResponse
from app.core.logging import logger

router = APIRouter(prefix="/saved-queries", tags=["saved-queries"])

# For now, we'll use mock IDs
MOCK_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")
MOCK_ORG_ID = UUID("550e8400-e29b-41d4-a716-446655440002")


@router.get("", response_model=APIResponse[list[SavedQueryResponse]])
def get_saved_queries(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    logger.info(f"Getting saved queries (skip={skip}, limit={limit})")
    try:
        repo = SavedQueryRepository(db)
        queries = repo.get_by_user_id(MOCK_USER_ID, skip, limit)
        logger.info(f"Retrieved {len(queries)} saved queries")
        return APIResponse(data=[SavedQueryResponse.model_validate(q) for q in queries])
    except Exception as e:
        logger.error(f"Failed to get saved queries: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get saved queries: {str(e)}")


@router.post("", response_model=APIResponse[SavedQueryResponse])
def create_saved_query(
    request: SavedQueryCreate, db: Session = Depends(get_db)
):
    logger.info(f"Creating saved query: {request.name}")
    try:
        repo = SavedQueryRepository(db)
        saved_query = repo.create({
            **request.model_dump(),
            "user_id": MOCK_USER_ID,
            "organization_id": MOCK_ORG_ID
        })
        logger.info(f"Saved query created: {saved_query.id}")
        return APIResponse(data=SavedQueryResponse.model_validate(saved_query))
    except Exception as e:
        logger.error(f"Failed to create saved query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create saved query: {str(e)}")


@router.put("/{query_id}", response_model=APIResponse[SavedQueryResponse])
def update_saved_query(
    query_id: UUID, request: SavedQueryUpdate, db: Session = Depends(get_db)
):
    logger.info(f"Updating saved query: {query_id}")
    try:
        repo = SavedQueryRepository(db)
        saved_query = repo.get(query_id)
        if not saved_query:
            logger.warning(f"Saved query not found: {query_id}")
            raise HTTPException(status_code=404, detail="Saved query not found")
        updated_query = repo.update(saved_query, request.model_dump(exclude_unset=True))
        logger.info(f"Saved query updated: {query_id}")
        return APIResponse(data=SavedQueryResponse.model_validate(updated_query))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update saved query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update saved query: {str(e)}")


@router.delete("/{query_id}", response_model=APIResponse[dict])
def delete_saved_query(
    query_id: UUID, db: Session = Depends(get_db)
):
    logger.info(f"Deleting saved query: {query_id}")
    try:
        repo = SavedQueryRepository(db)
        repo.remove(query_id)
        logger.info(f"Saved query deleted: {query_id}")
        return APIResponse(data={"message": "Saved query deleted successfully"})
    except Exception as e:
        logger.error(f"Failed to delete saved query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete saved query: {str(e)}")


@router.patch("/{query_id}/favorite", response_model=APIResponse[SavedQueryResponse])
def toggle_favorite(
    query_id: UUID, db: Session = Depends(get_db)
):
    logger.info(f"Toggling favorite for saved query: {query_id}")
    try:
        repo = SavedQueryRepository(db)
        saved_query = repo.get(query_id)
        if not saved_query:
            logger.warning(f"Saved query not found: {query_id}")
            raise HTTPException(status_code=404, detail="Saved query not found")
        updated_query = repo.update(saved_query, {"is_favorite": not saved_query.is_favorite})
        logger.info(f"Favorite toggled for: {query_id}")
        return APIResponse(data=SavedQueryResponse.model_validate(updated_query))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to toggle favorite: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to toggle favorite: {str(e)}")
