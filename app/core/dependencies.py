from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.clients.albums_client import AlbumsClient
from app.core.exceptions import InvalidTokenException, UnauthorizedAdminAccessException
from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repositories import UserRepository


bearer_scheme = HTTPBearer()
bearer_scheme_optional = HTTPBearer(auto_error=False)


def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme_optional),
    db: Session = Depends(get_db),
) -> User | None:
    if not credentials:
        return None
    try:
        token_data = decode_access_token(credentials.credentials)
        user_id = token_data.get("sub")
        if not user_id:
            return None
        return UserRepository(db).get_user_by_id(int(user_id))
    except Exception:
        return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    token_data = decode_access_token(credentials.credentials)
    user_id = token_data.get("sub")

    if not user_id:
        raise InvalidTokenException("Invalid token")

    user_repository = UserRepository(db)
    user = user_repository.get_user_by_id(int(user_id))

    if user is None:
        raise InvalidTokenException("Invalid token")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise UnauthorizedAdminAccessException()
    return current_user


def get_albums_client(request: Request) -> AlbumsClient:
    return request.app.state.albums_client
