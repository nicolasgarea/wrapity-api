from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.favorite_repositories import FavoriteRepository
from app.schemas.favorite_schemas import (
    FavoriteCreate,
    FavoriteResponse,
    FavoriteUpdate,
)
from app.services.favorite_services import FavoriteService


router = APIRouter(prefix="/favorites", tags=["favorites"])


def get_favorite_service(db: Session = Depends(get_db)) -> FavoriteService:
    repo = FavoriteRepository(db)
    return FavoriteService(repo)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=FavoriteResponse)
def add_favorite(
    favorite_schema: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:
    favorite = favorite_service.add_favorite(favorite_schema, current_user.id)
    return favorite


@router.get("/user/{user_id}", response_model=list[FavoriteResponse])
def get_favorites_by_user(
    user_id: int, favorite_service: FavoriteService = Depends(get_favorite_service)
) -> list[FavoriteResponse]:
    return favorite_service.get_user_favorites(user_id)


@router.patch("/{favorite_id}", response_model=FavoriteResponse)
def update_favorite(
    favorite_id: int,
    favorite_schema: FavoriteUpdate,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:
    favorite = favorite_service.update_favorite(
        current_user.id, favorite_id, favorite_schema
    )
    return favorite


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> None:
    favorite_service.delete_favorite(favorite_id, current_user.id)
