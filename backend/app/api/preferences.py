from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.session import get_db
from app.repositories.user_preferences import UserPreferencesRepository
from app.schemas.user_preferences import UserPreferencesBase, UserPreferencesUpdate, UserPreferencesResponse
from app.core.responses import APIResponse
from app.core.logging import logger

router = APIRouter(prefix="/preferences", tags=["preferences"])

# For now, we'll use a mock user ID
MOCK_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440000")


@router.get("", response_model=APIResponse[UserPreferencesResponse])
def get_preferences(db: Session = Depends(get_db)):
    repo = UserPreferencesRepository(db)
    prefs = repo.get_by_user_id(MOCK_USER_ID)
    if not prefs:
        prefs = repo.create({
            "user_id": MOCK_USER_ID,
            "theme": "light",
            "dashboard_settings": {},
            "saved_filters": [],
            "preferred_chart_type": "bar"
        })
    return APIResponse(data=UserPreferencesResponse.model_validate(prefs))


@router.put("", response_model=APIResponse[UserPreferencesResponse])
def update_preferences(request: UserPreferencesUpdate, db: Session = Depends(get_db)):
    repo = UserPreferencesRepository(db)
    prefs = repo.get_by_user_id(MOCK_USER_ID)
    if not prefs:
        prefs = repo.create({
            **UserPreferencesBase().model_dump(),
            "user_id": MOCK_USER_ID
        })
    updated_prefs = repo.update(prefs, request.model_dump(exclude_unset=True))
    return APIResponse(data=UserPreferencesResponse.model_validate(updated_prefs))
