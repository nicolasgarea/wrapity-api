from app.core.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    UsernameAlreadyExistsException,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.user_schemas import UserLogin, UserRegister


class Auth:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _validate_user_does_not_exist(self, user_data: UserRegister) -> None:
        if self.user_repository.get_user_by_email(user_data.email) is not None:
            raise EmailAlreadyExistsException("Email already exists")
        if self.user_repository.get_user_by_username(user_data.username) is not None:
            raise UsernameAlreadyExistsException("Username already exists")

    def register_user(self, user_data: UserRegister) -> str:
        self._validate_user_does_not_exist(user_data)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )
        self.user_repository.create_user(user)
        user_login = UserLogin(email=user_data.email, password=user_data.password)
        return self.login_user(user_login)

    def login_user(self, user_data: UserLogin) -> str:
        user = self.user_repository.get_user_by_email(user_data.email)
        if user is None:
            raise InvalidCredentialsException("Invalid email or password")
        if not verify_password(user_data.password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")
        return create_access_token({"sub": str(user.id)})
