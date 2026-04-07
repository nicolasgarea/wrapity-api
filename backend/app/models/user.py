from sqlalchemy import Column, Enum, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    bio = Column(String(300), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    role = Column(
        Enum("user", "admin", name="user_role"), nullable=False, server_default="user"
    )
    created_at = Column(DateTime, server_default=func.now())

    reviews = relationship("Review", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
