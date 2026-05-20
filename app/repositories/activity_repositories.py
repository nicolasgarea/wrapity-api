from sqlalchemy.orm import Session, joinedload

from app.models.activity import Activity
from app.models.follower import Follower
from app.models.review import Review


class ActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, activity: Activity) -> Activity:
        self.db.add(activity)
        self.db.commit()
        self.db.refresh(activity)
        return activity

    def get_following_feed(
        self, user_id: int, limit: int = 20, offset: int = 0
    ) -> list[Activity]:
        return (
            self.db.query(Activity)
            .options(
                joinedload(Activity.actor),
                joinedload(Activity.target_user),
                joinedload(Activity.review).joinedload(Review.user),
            )
            .join(Follower, Follower.followed_id == Activity.user_id)
            .filter(Follower.follower_id == user_id)
            .order_by(Activity.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
