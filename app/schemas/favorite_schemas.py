from pydantic import BaseModel, ConfigDict

from app.schemas.album_schemas import Album
from app.schemas.common import UtcDatetime


class FavoriteCreate(BaseModel):
    album_id: str
    position: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    album_id: str
    created_at: UtcDatetime
    position: int

    model_config = ConfigDict(from_attributes=True)


class FavoriteWithAlbumResponse(BaseModel):
    id: int
    user_id: int
    album_id: str
    position: int
    created_at: UtcDatetime
    album: Album

    model_config = ConfigDict(from_attributes=True)


class FavoriteUpdate(BaseModel):
    position: int | None = None


class FavoriteItemInput(BaseModel):
    album_id: str
    position: int


class FavoritesReplaceRequest(BaseModel):
    favorites: list[FavoriteItemInput]
