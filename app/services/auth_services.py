from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    UsernameAlreadyExistsException,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repositories import UserRepository


class Auth:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _validate_user_does_not_exist(self, email: str, username: str) -> None:
        if self.user_repository.get_user_by_email(email) is not None:
            raise EmailAlreadyExistsException("Email already exists")
        if self.user_repository.get_user_by_username(username) is not None:
            raise UsernameAlreadyExistsException("Username already exists")

    def register_user(self, username: str, email: str, password: str) -> str:
        self._validate_user_does_not_exist(email, username)
        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        self.user_repository.create_user(user)
        return self.login_user(email, password)

    def login_user(self, email: str, password: str) -> str:
        user = self.user_repository.get_user_by_email(email)
        if user is None:
            raise InvalidCredentialsException("Invalid email or password")
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")
        return create_access_token({"sub": str(user.id)})
