from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.clients.albums_client import AlbumsClient
from app.core.dependencies import get_albums_client, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.favorite_repositories import FavoriteRepository
from app.schemas.favorite_schemas import (
    FavoriteCreate,
    FavoriteResponse,
    FavoritesReplaceRequest,
    FavoriteUpdate,
    FavoriteWithAlbumResponse,
)
from app.services.favorite_services import FavoriteService


router = APIRouter(prefix="/favorites", tags=["favorites"])


def get_favorite_service(
    db: Session = Depends(get_db),
    albums_client: AlbumsClient = Depends(get_albums_client),
) -> FavoriteService:
    repo = FavoriteRepository(db)
    return FavoriteService(repo, albums_client)


def get_favorite_repository(db: Session = Depends(get_db)) -> FavoriteRepository:
    return FavoriteRepository(db)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=FavoriteResponse,
    responses={401: {"description": "Not authenticated"}},
)
def add_favorite(
    favorite_schema: FavoriteCreate,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:
    return favorite_service.add_favorite(
        favorite_schema.album_id, favorite_schema.position, current_user.id
    )


@router.put(
    "/me",
    response_model=list[FavoriteWithAlbumResponse],
    responses={401: {"description": "Not authenticated"}},
)
async def replace_my_favorites(
    request: FavoritesReplaceRequest,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> list[FavoriteWithAlbumResponse]:
    favorite_service.replace_favorites(current_user.id, request.favorites)
    return await favorite_service.get_user_favorites(current_user.id)


@router.get(
    "/user/{user_id}",
    response_model=list[FavoriteWithAlbumResponse],
)
async def get_favorites_by_user(
    user_id: int,
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> list[FavoriteWithAlbumResponse]:
    return await favorite_service.get_user_favorites(user_id)


@router.patch("/{favorite_id}", response_model=FavoriteResponse)
def update_favorite(
    favorite_id: int,
    favorite_schema: FavoriteUpdate,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> FavoriteResponse:
    return favorite_service.update_favorite(
        current_user.id, favorite_id, favorite_schema.position
    )


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(
    favorite_id: int,
    current_user: User = Depends(get_current_user),
    favorite_service: FavoriteService = Depends(get_favorite_service),
) -> None:
    favorite_service.delete_favorite(favorite_id, current_user.id)
