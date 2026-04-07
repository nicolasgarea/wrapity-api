from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.review_repositories import ReviewRepository
from app.schemas.review_schemas import ReviewCreate, ReviewResponse, ReviewUpdate
from app.services.review_services import ReviewService


router = APIRouter(prefix="/reviews", tags=["review"])


def get_review_service(db: Session = Depends(get_db)) -> ReviewService:
    repo = ReviewRepository(db)
    return ReviewService(repo)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReviewResponse)
def create(
    review_schema: ReviewCreate,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:

    review = review_service.create(
        review_schema.album_id,
        review_schema.rating,
        review_schema.content,
        current_user.id,
    )
    return review


@router.get("/me", response_model=list[ReviewResponse])
def get_my_reviews(
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> list[ReviewResponse]:

    reviews = review_service.get_by_user_id(current_user.id)
    return reviews


@router.get("/album/{album_id}", response_model=list[ReviewResponse])
def get_reviews_by_album(
    album_id: str, review_service: ReviewService = Depends(get_review_service)
) -> list[ReviewResponse]:

    reviews = review_service.get_by_album_id(album_id)
    return reviews


@router.get("/user/{user_id}", response_model=list[ReviewResponse])
def get_reviews_by_user(
    user_id: int, review_service: ReviewService = Depends(get_review_service)
) -> list[ReviewResponse]:
    reviews = review_service.get_by_user_id(user_id)
    return reviews


@router.patch("/{review_id}", response_model=ReviewResponse)
def update_review(
    review_schema: ReviewUpdate,
    review_id: int,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    review = review_service.update(
        user_id=current_user.id,
        review_id=review_id,
        rating=review_schema.rating,
        content=review_schema.content,
    )
    return review


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    review_service: ReviewService = Depends(get_review_service),
) -> None:
    review_service.delete(user_id=current_user.id, review_id=review_id)
