import asyncio

from app.clients.albums_client import AlbumsClient
from app.models.activity import Activity
from app.repositories.activity_repositories import ActivityRepository
from app.repositories.like_repositories import LikeRepository
from app.schemas.activity_schemas import ActivityFeedItemResponse
from app.schemas.album_schemas import Album
from app.schemas.review_schemas import ReviewFeedItemResponse
from app.schemas.user_schemas import UserPublicResponse


class ActivityService:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        albums_client: AlbumsClient,
        like_repository: LikeRepository,
    ):
        self.activity_repository = activity_repository
        self.albums_client = albums_client
        self.like_repository = like_repository

    async def get_following_feed(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[ActivityFeedItemResponse]:
        activities = self.activity_repository.get_following_feed(
            user_id=user_id, limit=limit, offset=offset
        )
        return await self._build_feed(activities, current_user_id=user_id)

    async def _build_feed(
        self, activities: list[Activity], current_user_id: int | None = None
    ) -> list[ActivityFeedItemResponse]:
        if not activities:
            return []

        album_ids = {a.review.album_id for a in activities if a.review is not None}
        albums_by_id = await self._fetch_albums(album_ids)

        review_ids = [a.review.id for a in activities if a.review is not None]
        likes_by_review = self.like_repository.count_for_reviews(review_ids)
        liked_ids = (
            self.like_repository.liked_review_ids(current_user_id, review_ids)
            if current_user_id is not None
            else set()
        )

        items: list[ActivityFeedItemResponse] = []
        for a in activities:
            review_item = None
            if a.review is not None:
                album = albums_by_id.get(a.review.album_id)
                if album is None:
                    continue
                review_item = ReviewFeedItemResponse(
                    id=a.review.id,
                    rating=a.review.rating,
                    content=a.review.content,
                    created_at=a.review.created_at,
                    updated_at=a.review.updated_at,
                    album=album,
                    author=UserPublicResponse.model_validate(a.review.user),
                    likes_count=likes_by_review.get(a.review.id, 0),
                    liked_by_me=a.review.id in liked_ids,
                )

            items.append(
                ActivityFeedItemResponse(
                    id=a.id,
                    type=a.type,
                    created_at=a.created_at,
                    actor=UserPublicResponse.model_validate(a.actor),
                    review=review_item,
                    target_user=(
                        UserPublicResponse.model_validate(a.target_user)
                        if a.target_user is not None
                        else None
                    ),
                )
            )

        return items

    async def _fetch_albums(self, album_ids: set[int]) -> dict[int, Album]:
        if not album_ids:
            return {}

        albums_raw = await asyncio.gather(
            *[self.albums_client.get_album_by_id(aid) for aid in album_ids],
            return_exceptions=True,
        )

        albums_by_id: dict[int, Album] = {}
        for raw in albums_raw:
            if isinstance(raw, Exception) or not raw or "id" not in raw:
                continue
            albums_by_id[int(raw["id"])] = Album(**raw)
        return albums_by_id
