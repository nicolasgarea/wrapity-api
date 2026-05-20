from datetime import datetime

from pydantic import BaseModel

from app.schemas.review_schemas import ReviewFeedItemResponse
from app.schemas.user_schemas import UserPublicResponse


class ActivityFeedItemResponse(BaseModel):
    id: int
    type: str
    created_at: datetime
    actor: UserPublicResponse
    review: ReviewFeedItemResponse | None = None
    target_user: UserPublicResponse | None = None


class ActivityFeedResponse(BaseModel):
    items: list[ActivityFeedItemResponse]
