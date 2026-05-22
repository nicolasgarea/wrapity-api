from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload
from app.models.follower import Follower
from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_by_user_id(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[Review]:
        return (
            self.db.query(Review)
            .options(joinedload(Review.user))
            .filter_by(user_id=user_id)
            .order_by(Review.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_by_album_id(
        self, album_id: str, limit: int = 20, offset: int = 0
    ) -> list[Review]:
        return (
            self.db.query(Review)
            .options(joinedload(Review.user))
            .filter(Review.album_id == album_id)
            .order_by(Review.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_by_id(self, review_id: int) -> Review:
        review = self.db.query(Review).filter_by(id=review_id).first()
        return review

    def update(self, review: Review, rating: int | None, content: str | None) -> Review:
        if content is not None:
            review.content = content
        if rating is not None:
            review.rating = rating
        if rating or content:
            review.updated_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(review)
        return review

    def get_following_feed(
        self, user_id: int, limit: int, offset: int = 0
    ) -> list[Review]:
        return (
            self.db.query(Review)
            .options(joinedload(Review.user))
            .join(Follower, Follower.followed_id == Review.user_id)
            .filter(Follower.follower_id == user_id)
            .order_by(Review.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def get_recent(self, limit: int = 20, offset: int = 0) -> list[Review]:
        return (
            self.db.query(Review)
            .options(joinedload(Review.user))
            .order_by(Review.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

    def delete(self, review: Review) -> None:
        self.db.delete(review)
        self.db.commit()
