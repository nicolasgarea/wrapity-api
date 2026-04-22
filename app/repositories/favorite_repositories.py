from sqlalchemy.orm import Session

from app.models.favorite import Favorite


class FavoriteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, favorite: Favorite) -> Favorite:
        self.db.add(favorite)
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def get_by_user_id(self, user_id: int) -> list[Favorite]:
        favorites = self.db.query(Favorite).filter_by(user_id=user_id).all()
        return favorites

    def get_by_id(self, favorite_id: int) -> Favorite:
        favorite = self.db.query(Favorite).filter_by(id=favorite_id).first()
        return favorite

    def count_by_album_id(self, album_id: int) -> int:
        return self.db.query(Favorite).filter_by(album_id=album_id).count()

    def update(self, favorite: Favorite, position: int) -> Favorite:
        favorite.position = position
        self.db.commit()
        self.db.refresh(favorite)
        return favorite

    def delete(self, favorite: Favorite) -> None:
        self.db.delete(favorite)
        self.db.commit()
