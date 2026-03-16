from app.schemas.review_schemas import ReviewUpdate
from sqlalchemy.orm import Session
from app.models.review import Review


class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def get_by_user_id(self, user_id: int) -> list[Review]:
        reviews = self.db.query(Review).filter_by(user_id=user_id).all()
        return reviews

    def get_by_album_id(self, album_id: str) -> list[Review]:
        reviews = self.db.query(Review).filter_by(album_id=album_id).all()
        return reviews

    def get_by_id(self, review_id: int) -> Review:
        review = self.db.query(Review).filter_by(id=review_id).first()
        return review

    def update(self, review: Review, review_update: ReviewUpdate) -> Review:
        if review_update.content is not None:
            review.content = review_update.content
        if review_update.rating is not None:
            review.rating = review_update.rating

        self.db.commit()
        self.db.refresh(review)
        return review

    def delete(self, review: Review) -> None:
        self.db.delete(review)
        self.db.commit()
