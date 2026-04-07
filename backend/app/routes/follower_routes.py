from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.follower_repositories import FollowerRepository
from app.schemas.follower_schemas import FollowerResponse
from app.services.follower_services import FollowerService


router = APIRouter(prefix="/users", tags=["followers"])


def get_follower_service(db: Session = Depends(get_db)) -> FollowerService:
    repo = FollowerRepository(db)
    return FollowerService(repo)


@router.post(
    "/{user_id}/follow",
    status_code=status.HTTP_201_CREATED,
    response_model=FollowerResponse,
)
def follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    follower_service: FollowerService = Depends(get_follower_service),
) -> FollowerResponse:
    return follower_service.follow(current_user.id, user_id)


@router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
def unfollow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    follower_service: FollowerService = Depends(get_follower_service),
) -> None:
    follower_service.unfollow(current_user.id, user_id)


@router.get("/{user_id}/followers", response_model=list[FollowerResponse])
def get_followers(
    user_id: int,
    follower_service: FollowerService = Depends(get_follower_service),
) -> list[FollowerResponse]:
    return follower_service.get_followers(user_id)


@router.get("/{user_id}/following", response_model=list[FollowerResponse])
def get_following(
    user_id: int,
    follower_service: FollowerService = Depends(get_follower_service),
) -> list[FollowerResponse]:
    return follower_service.get_following(user_id)
