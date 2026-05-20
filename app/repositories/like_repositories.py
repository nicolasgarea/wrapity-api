from sqlalchemy import func

from sqlalchemy.orm import Session

from app.models.like import Like


class LikeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, like: Like) -> Like:
        self.db.add(like)
        self.db.commit()
        self.db.refresh(like)
        return like

    def get_by_user_and_review(self, user_id: int, review_id: int) -> Like | None:
        return (
            self.db.query(Like).filter_by(user_id=user_id, review_id=review_id).first()
        )

    def count_by_review(self, review_id: int) -> int:
        return self.db.query(Like).filter_by(review_id=review_id).count()

    def count_for_reviews(self, review_ids: list[int]) -> dict[int, int]:
        if not review_ids:
            return {}
        rows = (
            self.db.query(Like.review_id, func.count(Like.id))
            .filter(Like.review_id.in_(review_ids))
            .group_by(Like.review_id)
            .all()
        )
        return {review_id: count for review_id, count in rows}

    def liked_review_ids(self, user_id: int, review_ids: list[int]) -> set[int]:
        if not review_ids:
            return set()
        rows = (
            self.db.query(Like.review_id)
            .filter(Like.user_id == user_id, Like.review_id.in_(review_ids))
            .all()
        )
        return {row[0] for row in rows}

    def delete(self, like: Like) -> None:
        self.db.delete(like)
        self.db.commit()
