import asyncio

from app.clients.albums_client import AlbumsClient
from app.core.exceptions import (
    ReviewNotFoundException,
    UnauthorizedReviewAccessException,
)
from app.models.activity import Activity
from app.models.review import Review
from app.repositories.activity_repositories import ActivityRepository
from app.repositories.like_repositories import LikeRepository
from app.repositories.review_repositories import ReviewRepository
from app.schemas.album_schemas import Album
from app.schemas.review_schemas import ReviewFeedItemResponse
from app.schemas.user_schemas import UserPublicResponse


class ReviewService:
    def __init__(
        self,
        review_repository: ReviewRepository,
        albums_client: AlbumsClient,
        activity_repository: ActivityRepository,
        like_repository: LikeRepository,
    ):
        self.review_repository = review_repository
        self.albums_client = albums_client
        self.activity_repository = activity_repository
        self.like_repository = like_repository

    def create(self, album_id: str, rating: int, content: str, user_id: int) -> Review:
        review = Review(
            user_id=user_id,
            album_id=album_id,
            rating=rating,
            content=content,
        )
        self.review_repository.create(review)
        self.activity_repository.create(
            Activity(user_id=user_id, type="review", review_id=review.id)
        )
        return review

    async def get_by_album_id(
        self,
        album_id: str,
        limit: int = 20,
        offset: int = 0,
        current_user_id: int | None = None,
    ) -> list[ReviewFeedItemResponse]:
        reviews = self.review_repository.get_by_album_id(
            album_id=album_id, limit=limit, offset=offset
        )
        return await self._embed_albums(reviews, current_user_id)

    async def get_by_user_id(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        current_user_id: int | None = None,
    ) -> list[ReviewFeedItemResponse]:
        reviews = self.review_repository.get_by_user_id(
            user_id=user_id, limit=limit, offset=offset
        )
        return await self._embed_albums(reviews, current_user_id)

    async def get_recent(
        self, limit: int = 20, offset: int = 0, current_user_id: int | None = None
    ) -> list[ReviewFeedItemResponse]:
        reviews = self.review_repository.get_recent(limit=limit, offset=offset)
        return await self._embed_albums(reviews, current_user_id)

    async def get_following_feed(
        self, user_id: int, limit: int, offset: int = 0
    ) -> list[ReviewFeedItemResponse]:
        reviews = self.review_repository.get_following_feed(
            user_id=user_id, limit=limit, offset=offset
        )
        return await self._embed_albums(reviews, current_user_id=user_id)

    def get_by_id(self, review_id: int) -> Review:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException()
        return review

    def update(
        self, user_id: int, review_id: int, rating: int | None, content: str | None
    ) -> Review:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException()
        if review.user_id != user_id:
            raise UnauthorizedReviewAccessException()
        return self.review_repository.update(
            review=review, rating=rating, content=content
        )

    def delete(self, user_id: int, review_id: int) -> None:
        review = self.review_repository.get_by_id(review_id)
        if not review:
            raise ReviewNotFoundException()
        if review.user_id != user_id:
            raise UnauthorizedReviewAccessException()
        self.review_repository.delete(review)

    async def _embed_albums(
        self, reviews: list[Review], current_user_id: int | None = None
    ) -> list[ReviewFeedItemResponse]:
        if not reviews:
            return []

        unique_album_ids = {r.album_id for r in reviews}

        albums_raw = await asyncio.gather(
            *[self.albums_client.get_album_by_id(aid) for aid in unique_album_ids],
            return_exceptions=True,
        )

        albums_by_id: dict[int, Album] = {}
        for raw in albums_raw:
            if isinstance(raw, Exception) or not raw or "id" not in raw:
                continue
            albums_by_id[int(raw["id"])] = Album(**raw)

        review_ids = [r.id for r in reviews]
        likes_by_review = self.like_repository.count_for_reviews(review_ids)
        liked_ids = (
            self.like_repository.liked_review_ids(current_user_id, review_ids)
            if current_user_id is not None
            else set()
        )

        feed: list[ReviewFeedItemResponse] = []
        for r in reviews:
            album = albums_by_id.get(r.album_id)
            if album is None:
                continue
            feed.append(
                ReviewFeedItemResponse(
                    id=r.id,
                    rating=r.rating,
                    content=r.content,
                    created_at=r.created_at,
                    updated_at=r.updated_at,
                    album=album,
                    author=UserPublicResponse.model_validate(r.user),
                    likes_count=likes_by_review.get(r.id, 0),
                    liked_by_me=r.id in liked_ids,
                )
            )

        return feed
