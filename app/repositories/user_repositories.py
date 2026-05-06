from sqlalchemy.orm import Session
from app.models.follower import Follower
from app.models.review import Review
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter_by(email=email).first()

    def get_user_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter_by(username=username).first()

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter_by(id=user_id).first()

    def update_user(
        self,
        db_user: User,
        username: str | None,
        bio: str | None,
        avatar_url: str | None,
    ) -> User:
        if username is not None:
            db_user.username = username
        if bio is not None:
            db_user.bio = bio
        if avatar_url is not None:
            db_user.avatar_url = avatar_url

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def count_reviews(self, user_id: int) -> int:
        return self.db.query(Review).filter_by(user_id=user_id).count()

    def count_followers(self, user_id: int) -> int:
        return self.db.query(Follower).filter_by(followed_id=user_id).count()

    def count_following(self, user_id: int) -> int:
        return self.db.query(Follower).filter_by(follower_id=user_id).count()

    def is_following(self, follower_id: int, followed_id: int) -> bool:
        return (
            self.db.query(Follower)
            .filter_by(
                follower_id=follower_id,
                followed_id=followed_id,
            )
            .first()
            is not None
        )

    def search(self, query: str, limit: int = 20) -> list[User]:
        return (
            self.db.query(User)
            .filter(User.username.ilike(f"%{query}%"))
            .order_by(User.username)
            .limit(limit)
            .all()
        )
