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
