from app.clients.cloudinary_client import CloudinaryClient
from app.core.exceptions import UserNotFoundException
from app.models.user import User
from app.repositories.user_repositories import UserRepository


class UserService:
    def __init__(
        self, user_repository: UserRepository, cloudinary_client: CloudinaryClient
    ):
        self.user_repository = user_repository
        self.cloudinary_client = cloudinary_client

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

    def upload_avatar(self, current_user: User, file: bytes) -> User:
        avatar_url = self.cloudinary_client.upload_avatar(
            file, public_id=str(current_user.id)
        )
        return self.user_repository.update_user(current_user, None, None, avatar_url)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        return user
