from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    review_id = Column(
        Integer, ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="likes")
    review = relationship("Review", back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "review_id", name="uq_like_user_review"),
    )
