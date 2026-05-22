from app.core.exceptions import (
    AlreadyLikedException,
    LikeNotFoundException,
    ReviewNotFoundException,
)
from app.models.activity import Activity
from app.models.like import Like
from app.repositories.activity_repositories import ActivityRepository
from app.repositories.like_repositories import LikeRepository
from app.repositories.review_repositories import ReviewRepository


class LikeService:
    def __init__(
        self,
        like_repository: LikeRepository,
        review_repository: ReviewRepository,
        activity_repository: ActivityRepository,
    ):
        self.like_repository = like_repository
        self.review_repository = review_repository
        self.activity_repository = activity_repository

    def like(self, user_id: int, review_id: int) -> Like:
        if self.review_repository.get_by_id(review_id) is None:
            raise ReviewNotFoundException()

        existing = self.like_repository.get_by_user_and_review(user_id, review_id)
        if existing is not None:
            raise AlreadyLikedException()

        like = self.like_repository.create(Like(user_id=user_id, review_id=review_id))
        self.activity_repository.create(
            Activity(user_id=user_id, type="like", review_id=review_id)
        )
        return like

    def unlike(self, user_id: int, review_id: int) -> None:
        like = self.like_repository.get_by_user_and_review(user_id, review_id)
        if like is None:
            raise LikeNotFoundException()
        self.like_repository.delete(like)

    def get_like_count(self, review_id: int) -> int:
        if self.review_repository.get_by_id(review_id) is None:
            raise ReviewNotFoundException()
        return self.like_repository.count_by_review(review_id)
