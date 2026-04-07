from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Follower(Base):
    __tablename__ = "followers"

    follower_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    followed_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    created_at = Column(DateTime, server_default=func.now())

    follower = relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    followed = relationship(
        "User", foreign_keys=[followed_id], back_populates="followers"
    )
