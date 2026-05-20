from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.activity_repositories import ActivityRepository
from app.repositories.like_repositories import LikeRepository
from app.repositories.review_repositories import ReviewRepository
from app.schemas.like_schemas import LikeCountResponse, LikeResponse
from app.services.like_services import LikeService


router = APIRouter(prefix="/reviews", tags=["likes"])


def get_like_service(db: Session = Depends(get_db)) -> LikeService:
    return LikeService(
        like_repository=LikeRepository(db),
        review_repository=ReviewRepository(db),
        activity_repository=ActivityRepository(db),
    )


@router.post(
    "/{review_id}/like",
    status_code=status.HTTP_201_CREATED,
    response_model=LikeResponse,
    responses={401: {"description": "Not authenticated"}},
)
def like_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service),
) -> LikeResponse:
    return like_service.like(current_user.id, review_id)


@router.delete("/{review_id}/like", status_code=status.HTTP_204_NO_CONTENT)
def unlike_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    like_service: LikeService = Depends(get_like_service),
) -> None:
    like_service.unlike(current_user.id, review_id)


@router.get("/{review_id}/likes/count", response_model=LikeCountResponse)
def get_like_count(
    review_id: int,
    like_service: LikeService = Depends(get_like_service),
) -> LikeCountResponse:
    count = like_service.get_like_count(review_id)
    return LikeCountResponse(review_id=review_id, likes_count=count)
