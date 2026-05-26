from pydantic import BaseModel, ConfigDict

from app.schemas.common import UtcDatetime


class FollowerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    follower_id: int
    followed_id: int
    created_at: UtcDatetime
