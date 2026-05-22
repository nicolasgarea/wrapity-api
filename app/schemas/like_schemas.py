from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LikeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    review_id: int
    created_at: datetime


class LikeCountResponse(BaseModel):
    review_id: int
    likes_count: int
