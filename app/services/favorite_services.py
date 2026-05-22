from app.clients.albums_client import AlbumsClient
from app.core.exceptions import (
    AlbumAlreadyInFavoritesException,
    FavoriteNotFoundException,
    FavoriteSlotAlreadyOccupedException,
    InvalidFavoritePositionException,
    UnauthorizedFavoriteAccessException,
)
from app.models.favorite import Favorite
from app.repositories.favorite_repositories import FavoriteRepository
from app.schemas.album_schemas import Album
from app.schemas.favorite_schemas import (
    FavoriteItemInput,
    FavoriteWithAlbumResponse,
)


class FavoriteService:
    def __init__(
        self,
        favorite_repository: FavoriteRepository,
        albums_client: AlbumsClient,
    ):
        self.favorite_repository = favorite_repository
        self.albums_client = albums_client

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

    async def get_user_favorites(self, user_id: int) -> list[FavoriteWithAlbumResponse]:
        favorites = self.favorite_repository.get_by_user_id(user_id)

        result = []
        for f in favorites:
            album_data = await self.albums_client.get_album_by_id(int(f.album_id))
            result.append(
                FavoriteWithAlbumResponse(
                    id=f.id,
                    user_id=f.user_id,
                    album_id=f.album_id,
                    position=f.position,
                    created_at=f.created_at,
                    album=Album(**album_data),
                )
            )
        return result

    def replace_favorites(
        self, user_id: int, favorites: list[FavoriteItemInput]
    ) -> list[Favorite]:
        if len(favorites) > 4:
            raise InvalidFavoritePositionException()

        seen_positions = set()
        seen_albums = set()
        for f in favorites:
            if f.position < 1 or f.position > 4:
                raise InvalidFavoritePositionException()
            if f.position in seen_positions:
                raise FavoriteSlotAlreadyOccupedException()
            if f.album_id in seen_albums:
                raise AlbumAlreadyInFavoritesException()
            seen_positions.add(f.position)
            seen_albums.add(f.album_id)

        self.favorite_repository.delete_all_by_user_id(user_id)

        new_favorites = []
        for item in favorites:
            favorite = Favorite(
                user_id=user_id,
                album_id=item.album_id,
                position=item.position,
            )
            self.favorite_repository.create(favorite)
            new_favorites.append(favorite)

        return new_favorites

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
