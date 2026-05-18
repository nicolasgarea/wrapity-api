from app.clients.cloudinary_client import CloudinaryClient
from app.core.exceptions import UserNotFoundException
from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.user_schemas import UserProfileResponse


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

    def get_profile_by_username(
        self, username: str, viewer: User
    ) -> UserProfileResponse:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise UserNotFoundException()

        is_following = None
        if viewer is not None and viewer.id != user.id:
            is_following = self.user_repository.is_following(
                follower_id=viewer.id,
                followed_id=user.id,
            )

        return UserProfileResponse(
            id=user.id,
            username=user.username,
            bio=user.bio,
            avatar_url=user.avatar_url,
            reviews_count=self.user_repository.count_reviews(user.id),
            followers_count=self.user_repository.count_followers(user.id),
            following_count=self.user_repository.count_following(user.id),
            is_following=is_following,
        )

    def search_users(self, query: str, limit: int = 20) -> list[User]:
        query = query.strip()
        if not query:
            return []
        return self.user_repository.search(query, limit)
