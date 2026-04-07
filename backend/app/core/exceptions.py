class InvalidTokenException(Exception):
    pass


class EmailAlreadyExistsException(Exception):
    pass


class UsernameAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class ReviewNotFoundException(Exception):
    pass


class UnauthorizedReviewAccessException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class UnauthorizedFavoriteAccessException(Exception):
    pass


class FavoriteNotFoundException(Exception):
    pass


class InvalidFavoritePositionException(Exception):
    pass


class FavoriteSlotAlreadyOccupedException(Exception):
    pass


class AlbumAlreadyInFavoritesException(Exception):
    pass


class UnauthorizedAdminAccessException(Exception):
    pass
