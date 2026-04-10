from sqlalchemy.orm import Session

from app.models.follower import Follower


class FollowerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, follower: Follower) -> Follower:
        self.db.add(follower)
        self.db.commit()
        self.db.refresh(follower)
        return follower

    def get_by_follower_and_followed(
        self, follower_id: int, followed_id: int
    ) -> Follower | None:
        return (
            self.db.query(Follower)
            .filter_by(follower_id=follower_id, followed_id=followed_id)
            .first()
        )

    def get_followers(self, user_id: int) -> list[Follower]:
        return self.db.query(Follower).filter_by(followed_id=user_id).all()

    def get_following(self, user_id: int) -> list[Follower]:
        return self.db.query(Follower).filter_by(follower_id=user_id).all()

    def delete(self, follower: Follower) -> None:
        self.db.delete(follower)
        self.db.commit()
