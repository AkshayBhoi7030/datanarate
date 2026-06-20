from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.session import get_db
from app.models import User, UserRole, Organization
from app.schemas.user import UserCreate, UserResponse
from app.core.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user
)
from app.core.config import settings
from app.core.responses import APIResponse
from app.repositories.user import UserRepository
from app.repositories.organization import OrganizationRepository
from app.core.logging import logger

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=APIResponse[UserResponse])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    existing_user = user_repo.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create a default organization for the new user
    org_repo = OrganizationRepository(db)
    org = org_repo.create({
        "name": f"{user_data.full_name or user_data.email}'s Organization",
        "slug": user_data.email.split('@')[0].lower()
    })

    hashed_pw = get_password_hash(user_data.password)
    user = user_repo.create({
        "organization_id": org.id,
        "email": user_data.email,
        "hashed_password": hashed_pw,
        "full_name": user_data.full_name,
        "role": UserRole.ADMIN
    })

    logger.info(f"User registered: {user.email}")
    return APIResponse(data=UserResponse.model_validate(user))


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    logger.info(f"User logged in: {user.email}")
    return APIResponse(data={"access_token": access_token, "token_type": "bearer"})


@router.get("/me", response_model=APIResponse[UserResponse])
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return APIResponse(data=UserResponse.model_validate(current_user))
