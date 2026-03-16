from app.core.exceptions import UserNotFoundException
from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.user_schemas import UserProfileResponse, UserResponse, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def update_user(self, current_user: User, user_update: UserUpdate) -> UserResponse:
        updated_user = self.user_repository.update_user(current_user, user_update)
        return updated_user

    def get_user_by_id(self, user_id: int) -> UserProfileResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
