from app.core.exceptions import (
    AlreadyFollowingException,
    CannotFollowYourselfException,
    FollowNotFoundException,
    UserNotFoundException,
)
from app.models.follower import Follower
from app.repositories.follower_repositories import FollowerRepository
from app.repositories.user_repositories import UserRepository


class FollowerService:
    def __init__(
        self, follower_repository: FollowerRepository, user_repository: UserRepository
    ):
        self.follower_repository = follower_repository
        self.user_repository = user_repository

    def follow(self, follower_id: int, followed_id: int) -> Follower:
        if follower_id == followed_id:
            raise CannotFollowYourselfException()

        existing = self.follower_repository.get_by_follower_and_followed(
            follower_id, followed_id
        )
        if existing is not None:
            raise AlreadyFollowingException()

        if self.user_repository.get_user_by_id(followed_id) is None:
            raise UserNotFoundException()

        follower = Follower(follower_id=follower_id, followed_id=followed_id)
        return self.follower_repository.create(follower)

    def unfollow(self, follower_id: int, followed_id: int) -> None:
        follow = self.follower_repository.get_by_follower_and_followed(
            follower_id, followed_id
        )
        if follow is None:
            raise FollowNotFoundException()
        self.follower_repository.delete(follow)

    def get_followers(self, user_id: int) -> list[Follower]:
        return self.follower_repository.get_followers(user_id)

    def get_following(self, user_id: int) -> list[Follower]:
        return self.follower_repository.get_following(user_id)
