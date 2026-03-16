from app.core.exceptions import (
    AlbumAlreadyInFavoritesException,
    FavoriteNotFoundException,
    FavoriteSlotAlreadyOccupedException,
    InvalidFavoritePositionException,
    UnauthorizedFavoriteAccessException,
)
from app.models.favorite import Favorite
from app.repositories.favorite_repositories import FavoriteRepository
from app.schemas.favorite_schemas import FavoriteCreate, FavoriteUpdate


class FavoriteService:
    def __init__(self, favorite_repository: FavoriteRepository):
        self.favorite_repository = favorite_repository

    def add_favorite(self, favorite_create: FavoriteCreate, user_id: int) -> Favorite:
        if favorite_create.position < 1 or favorite_create.position > 4:
            raise InvalidFavoritePositionException()

        user_favorites = self.favorite_repository.get_by_user_id(user_id)

        for f in user_favorites:
            if favorite_create.album_id == f.album_id:
                raise AlbumAlreadyInFavoritesException()

            if favorite_create.position == f.position:
                raise FavoriteSlotAlreadyOccupedException()

        favorite = Favorite(
            user_id=user_id,
            album_id=favorite_create.album_id,
            position=favorite_create.position,
        )
        self.favorite_repository.create(favorite)
        return favorite

    def get_user_favorites(self, user_id: int) -> list[Favorite]:
        favorites = self.favorite_repository.get_by_user_id(user_id)
        return favorites

    def update_favorite(
        self, user_id: int, favorite_id: int, favorite_update: FavoriteUpdate
    ) -> Favorite:
        favorite = self.favorite_repository.get_by_id(favorite_id)
        if favorite is None:
            raise FavoriteNotFoundException()
        if favorite.user_id != user_id:
            raise UnauthorizedFavoriteAccessException()

        user_favorites = self.favorite_repository.get_by_user_id(user_id)
        for f in user_favorites:
            if f.position == favorite_update.position:
                swap_update = FavoriteUpdate(position=favorite.position)
                self.favorite_repository.update(f, swap_update)
                break

        updated_favorite = self.favorite_repository.update(favorite, favorite_update)
        return updated_favorite

    def delete_favorite(self, favorite_id: int, user_id: int):
        favorite = self.favorite_repository.get_by_id(favorite_id)
        if not favorite:
            raise FavoriteNotFoundException()
        if favorite.user_id != user_id:
            raise UnauthorizedFavoriteAccessException()
        self.favorite_repository.delete(favorite)
