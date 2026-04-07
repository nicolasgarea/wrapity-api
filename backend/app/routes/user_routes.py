from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.user_schemas import UserResponse, UserUpdate
from app.services.user_services import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    updated_user = user_service.update_user(
        current_user, user_update.username, user_update.bio, user_update.avatar_url
    )
    return updated_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    user = user_service.get_user_by_id(user_id)
    return user
