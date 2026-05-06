from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.album_schemas import Album


class FavoriteCreate(BaseModel):
    album_id: str
    position: int


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    album_id: str
    created_at: datetime
    position: int

    model_config = ConfigDict(from_attributes=True)


class FavoriteWithAlbumResponse(BaseModel):
    id: int
    user_id: int
    album_id: str
    position: int
    created_at: datetime
    album: Album

    model_config = ConfigDict(from_attributes=True)


class FavoriteUpdate(BaseModel):
    position: int | None = None


class FavoriteItemInput(BaseModel):
    album_id: str
    position: int


class FavoritesReplaceRequest(BaseModel):
    favorites: list[FavoriteItemInput]
