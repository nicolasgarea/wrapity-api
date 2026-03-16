from app.core.exceptions import (
    ReviewNotFoundException,
    UnauthorizedReviewAccessException,
)
from app.models.review import Review
from app.repositories.review_repositories import ReviewRepository
from app.schemas.review_schemas import ReviewCreate, ReviewUpdate


class ReviewService:
    def __init__(self, review_repository: ReviewRepository):
        self.review_repository = review_repository

    def create(self, review_schema: ReviewCreate, user_id: int) -> Review:
        review = Review(
            user_id=user_id,
            album_id=review_schema.album_id,
            rating=review_schema.rating,
            content=review_schema.content,
        )
        self.review_repository.create(review)
        return review

    def get_by_user_id(self, user_id: int) -> list[Review]:
        reviews = self.review_repository.get_by_user_id(user_id)
        return reviews

    def get_by_album_id(self, album_id: str) -> list[Review]:
        reviews = self.review_repository.get_by_album_id(album_id)
        return reviews

    def get_by_id(self, review_id: int) -> Review:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException()
        return review

    def update(self, user_id: int, review_id: int, review_update_schema: ReviewUpdate):
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException()
        if review.user_id != user_id:
            raise UnauthorizedReviewAccessException()
        review_updated = self.review_repository.update(
            review=review, review_update=review_update_schema
        )
        return review_updated

    def delete(self, user_id: int, review_id: int):
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException()
        if review.user_id != user_id:
            raise UnauthorizedReviewAccessException()
        self.review_repository.delete(review)
