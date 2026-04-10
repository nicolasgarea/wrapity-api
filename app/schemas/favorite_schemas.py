from datetime import datetime

from pydantic import BaseModel, ConfigDict


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


class FavoriteUpdate(BaseModel):
    position: int | None = None
