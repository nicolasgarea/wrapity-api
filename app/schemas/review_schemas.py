from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.album_schemas import Album
from app.schemas.user_schemas import UserPublicResponse


class ReviewCreate(BaseModel):
    album_id: int
    rating: int = Field(..., ge=1, le=5)
    content: str | None = None


class ReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    album_id: int
    rating: int
    content: str | None = None
    created_at: datetime
    updated_at: datetime


class ReviewUpdate(BaseModel):
    rating: int | None = Field(None, ge=1, le=5)
    content: str | None = None


class ReviewFeedItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    rating: int
    content: str | None = None
    created_at: datetime
    updated_at: datetime
    album: Album
    author: UserPublicResponse


class ReviewFeedResponse(BaseModel):
    items: list[ReviewFeedItemResponse]
