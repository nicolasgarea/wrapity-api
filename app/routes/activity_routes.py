from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.clients.albums_client import AlbumsClient
from app.core.dependencies import get_albums_client, get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.activity_repositories import ActivityRepository
from app.repositories.like_repositories import LikeRepository
from app.schemas.activity_schemas import ActivityFeedResponse
from app.services.activity_services import ActivityService


router = APIRouter(prefix="/activities", tags=["activity"])


def get_activity_service(
    db: Session = Depends(get_db),
    albums_client: AlbumsClient = Depends(get_albums_client),
) -> ActivityService:
    return ActivityService(ActivityRepository(db), albums_client, LikeRepository(db))


@router.get(
    "/following",
    response_model=ActivityFeedResponse,
    responses={401: {"description": "Not authenticated"}},
)
async def get_following_activity(
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    activity_service: ActivityService = Depends(get_activity_service),
) -> ActivityFeedResponse:
    items = await activity_service.get_following_feed(
        user_id=current_user.id, limit=limit, offset=offset
    )
    return ActivityFeedResponse(items=items)
