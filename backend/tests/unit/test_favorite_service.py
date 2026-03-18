from unittest.mock import MagicMock

from app.models.favorite import Favorite
from app.repositories.favorite_repositories import FavoriteRepository
from app.schemas.favorite_schemas import FavoriteUpdate
from app.services.favorite_services import FavoriteService
from app.core.exceptions import (
    FavoriteNotFoundException,
    UnauthorizedFavoriteAccessException,
)
import pytest


@pytest.fixture
def favorite_repository():
    return MagicMock(spec=FavoriteRepository)


@pytest.fixture
def favorite_service(favorite_repository):
    return FavoriteService(favorite_repository)


@pytest.fixture
def make_favorite():
    def _make_favorite(id, user_id, album_id, position):
        favorite = Favorite()
        favorite.id = id
        favorite.user_id = user_id
        favorite.album_id = album_id
        favorite.position = position
        return favorite

    return _make_favorite


def fake_update(favorite, update):
    favorite.position = update.position
    return favorite


def test_favorite_swap(favorite_repository, favorite_service, make_favorite):
    favorite_a = make_favorite(id=1, user_id=1, album_id="album-1", position=2)
    favorite_b = make_favorite(id=2, user_id=1, album_id="album-2", position=4)
    favorite_update = FavoriteUpdate(position=4)
    favorite_repository.get_by_id.return_value = favorite_a
    favorite_service.favorite_repository.get_by_user_id.return_value = [
        favorite_a,
        favorite_b,
    ]
    favorite_repository.update.side_effect = fake_update
    favorite_service.update_favorite(
        user_id=favorite_a.user_id,
        favorite_id=favorite_a.id,
        favorite_update=favorite_update,
    )
    assert favorite_a.position == 4
    assert favorite_b.position == 2


def test_update_not_found(favorite_repository, favorite_service, make_favorite):
    favorite = make_favorite(id=1, user_id=1, album_id="album-1", position=2)
    favorite_repository.get_by_id.return_value = None
    with pytest.raises(FavoriteNotFoundException):
        favorite_service.update_favorite(
            user_id=1,
            favorite_id=favorite.id,
            favorite_update=FavoriteUpdate(position=3),
        )


def test_delete_not_found(favorite_repository, favorite_service, make_favorite):
    favorite = make_favorite(id=1, user_id=1, album_id="album-1", position=2)
    favorite_repository.get_by_id.return_value = None
    with pytest.raises(FavoriteNotFoundException):
        favorite_service.delete_favorite(favorite_id=favorite.id, user_id=1)


def test_update_unauthorized(favorite_repository, favorite_service, make_favorite):
    favorite = make_favorite(id=1, user_id=1, album_id="album-1", position=2)
    favorite_repository.get_by_id.return_value = favorite
    with pytest.raises(UnauthorizedFavoriteAccessException):
        favorite_service.update_favorite(
            user_id=2,
            favorite_id=favorite.id,
            favorite_update=FavoriteUpdate(position=3),
        )


def test_delete_unauthorized(favorite_repository, favorite_service, make_favorite):
    favorite = make_favorite(id=1, user_id=1, album_id="album-1", position=2)
    favorite_repository.get_by_id.return_value = favorite
    with pytest.raises(UnauthorizedFavoriteAccessException):
        favorite_service.delete_favorite(favorite_id=favorite.id, user_id=2)
