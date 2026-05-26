from pydantic import BaseModel, ConfigDict

from app.schemas.common import UtcDatetime


class LikeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    review_id: int
    created_at: UtcDatetime


class LikeCountResponse(BaseModel):
    review_id: int
    likes_count: int
