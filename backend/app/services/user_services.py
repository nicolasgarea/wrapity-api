from app.core.exceptions import UserNotFoundException
from app.models.user import User
from app.repositories.user_repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def update_user(
        self,
        current_user: User,
        username: str | None,
        bio: str | None,
        avatar_url: str | None,
    ) -> User:
        updated_user = self.user_repository.update_user(
            current_user, username, bio, avatar_url
        )
        return updated_user

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
