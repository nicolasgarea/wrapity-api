from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    album_id = Column(String(100), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    position = Column(Integer, nullable=False)

    user = relationship("User", back_populates="favorites")

    __table_args__ = (
        UniqueConstraint("user_id", "album_id", name="uq_favorite_user_album"),
        UniqueConstraint("user_id", "position", name="uq_favorite_user_position"),
    )
