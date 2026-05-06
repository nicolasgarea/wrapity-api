from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.clients.albums_client import AlbumsClient
from app.core.dependencies import get_current_user, get_albums_client
from app.db.database import get_db
from app.models.user import User
from app.repositories.review_repositories import ReviewRepository
from app.schemas.review_schemas import (
    ReviewCreate,
    ReviewFeedItemResponse,
    ReviewFeedResponse,
    ReviewResponse,
    ReviewUpdate,
)
from app.services.review_services import ReviewService


router = APIRouter(prefix="/reviews", tags=["review"])


def get_review_service(
    db: Session = Depends(get_db),
    albums_client: AlbumsClient = Depends(get_albums_client),
) -> ReviewService:
    repo = ReviewRepository(db)
    return ReviewService(repo, albums_client)


@router.get(
    "/following",
    response_model=ReviewFeedResponse,
    responses={401: {"description": "Not authenticated"}},
)
async def get_following_feed(
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> ReviewFeedResponse:
    items = await review_service.get_following_feed(
        user_id=current_user.id, limit=limit, offset=offset
    )
    return ReviewFeedResponse(items=items)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewResponse,
    responses={401: {"description": "Not authenticated"}},
)
def create(
    review_schema: ReviewCreate,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    return review_service.create(
        review_schema.album_id,
        review_schema.rating,
        review_schema.content,
        current_user.id,
    )


@router.get(
    "/me",
    response_model=list[ReviewFeedItemResponse],
    responses={401: {"description": "Not authenticated"}},
)
async def get_my_reviews(
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> list[ReviewFeedItemResponse]:
    return await review_service.get_by_user_id(current_user.id)


@router.get("/album/{album_id}", response_model=list[ReviewFeedItemResponse])
async def get_reviews_by_album(
    album_id: str,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    review_service: ReviewService = Depends(get_review_service),
) -> list[ReviewFeedItemResponse]:
    return await review_service.get_by_album_id(
        album_id=album_id, limit=limit, offset=offset
    )


@router.get("/user/{user_id}", response_model=list[ReviewFeedItemResponse])
async def get_reviews_by_user(
    user_id: int,
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    review_service: ReviewService = Depends(get_review_service),
) -> list[ReviewFeedItemResponse]:
    return await review_service.get_by_user_id(
        user_id=user_id, limit=limit, offset=offset
    )


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_schema: ReviewUpdate,
    review_id: int,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    return review_service.update(
        user_id=current_user.id,
        review_id=review_id,
        rating=review_schema.rating,
        content=review_schema.content,
    )


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> None:
    review_service.delete(user_id=current_user.id, review_id=review_id)
