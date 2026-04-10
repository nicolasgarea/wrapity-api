from app.core.exceptions import (
    AlbumAlreadyInFavoritesException,
    FavoriteNotFoundException,
    FavoriteSlotAlreadyOccupedException,
    InvalidFavoritePositionException,
    UnauthorizedFavoriteAccessException,
)
from app.models.favorite import Favorite
from app.repositories.favorite_repositories import FavoriteRepository


class FavoriteService:
    def __init__(self, favorite_repository: FavoriteRepository):
        self.favorite_repository = favorite_repository

    def add_favorite(self, album_id: str, position: int, user_id: int) -> Favorite:
        if position < 1 or position > 4:
            raise InvalidFavoritePositionException()

        user_favorites = self.favorite_repository.get_by_user_id(user_id)

        for f in user_favorites:
            if album_id == f.album_id:
                raise AlbumAlreadyInFavoritesException()

            if position == f.position:
                raise FavoriteSlotAlreadyOccupedException()

        favorite = Favorite(
            user_id=user_id,
            album_id=album_id,
            position=position,
        )
        self.favorite_repository.create(favorite)
        return favorite

    def get_user_favorites(self, user_id: int) -> list[Favorite]:
        favorites = self.favorite_repository.get_by_user_id(user_id)
        return favorites

    def update_favorite(
        self, user_id: int, favorite_id: int, position: int
    ) -> Favorite:
        favorite = self.favorite_repository.get_by_id(favorite_id)
        if favorite is None:
            raise FavoriteNotFoundException()
        if favorite.user_id != user_id:
            raise UnauthorizedFavoriteAccessException()

        user_favorites = self.favorite_repository.get_by_user_id(user_id)
        for f in user_favorites:
            if f.position == position:
                self.favorite_repository.update(f, favorite.position)
                break

        return self.favorite_repository.update(favorite, position)

    def delete_favorite(self, favorite_id: int, user_id: int):
        favorite = self.favorite_repository.get_by_id(favorite_id)
        if not favorite:
            raise FavoriteNotFoundException()
        if favorite.user_id != user_id:
            raise UnauthorizedFavoriteAccessException()
        self.favorite_repository.delete(favorite)
