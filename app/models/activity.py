from sqlalchemy import Column, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    type = Column(
        Enum("review", "follow", "like", name="activity_type"), nullable=False
    )
    review_id = Column(
        Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=True
    )
    target_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    created_at = Column(DateTime, server_default=func.now())

    actor = relationship("User", foreign_keys=[user_id])
    target_user = relationship("User", foreign_keys=[target_user_id])
    review = relationship("Review")
