from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import (
    AlbumAlreadyInFavoritesException,
    AlbumNotFoundException,
    AlreadyFollowingException,
    AlreadyLikedException,
    CannotFollowYourselfException,
    CloudinaryUploadException,
    LikeNotFoundException,
    EmailAlreadyExistsException,
    FavoriteNotFoundException,
    FavoriteSlotAlreadyOccupedException,
    FollowNotFoundException,
    InvalidFavoritePositionException,
    ReviewNotFoundException,
    UnauthorizedAdminAccessException,
    UnauthorizedFavoriteAccessException,
    UnauthorizedReviewAccessException,
    UserNotFoundException,
    UsernameAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
)


def register_exception_handlers(app):

    @app.exception_handler(EmailAlreadyExistsException)
    def email_exists_handler(request: Request, exc: EmailAlreadyExistsException):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(UsernameAlreadyExistsException)
    def username_exists_handler(request: Request, exc: UsernameAlreadyExistsException):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(InvalidCredentialsException)
    def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(InvalidTokenException)
    def invalid_token_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(status_code=401, content={"detail": str(exc)})

    @app.exception_handler(ReviewNotFoundException)
    def review_not_found_handler(request: Request, exc: ReviewNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedReviewAccessException)
    def unauthorized_review_access_handler(
        request: Request, exc: UnauthorizedReviewAccessException
    ):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(UserNotFoundException)
    def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedFavoriteAccessException)
    def unauthorized_favorite_access_handler(
        request: Request, exc: UnauthorizedFavoriteAccessException
    ):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(FavoriteNotFoundException)
    def favorite_not_found_handler(request: Request, exc: FavoriteNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(InvalidFavoritePositionException)
    def invalid_favorite_position_handler(
        request: Request, exc: InvalidFavoritePositionException
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(AlbumAlreadyInFavoritesException)
    def album_already_in_favorites_handler(
        request: Request, exc: AlbumAlreadyInFavoritesException
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(FavoriteSlotAlreadyOccupedException)
    def favorite_slot_already_occupied_handler(
        request: Request, exc: FavoriteSlotAlreadyOccupedException
    ):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(UnauthorizedAdminAccessException)
    def unauthorized_admin_access_handler(
        request: Request, exc: UnauthorizedAdminAccessException
    ):
        return JSONResponse(
            status_code=403, content={"detail": "Admin access required"}
        )

    @app.exception_handler(AlreadyFollowingException)
    def already_following_handler(request: Request, exc: AlreadyFollowingException):
        return JSONResponse(
            status_code=409, content={"detail": "Already following this user"}
        )

    @app.exception_handler(FollowNotFoundException)
    def follow_not_found_handler(request: Request, exc: FollowNotFoundException):
        return JSONResponse(
            status_code=404, content={"detail": "Follow relationship not found"}
        )

    @app.exception_handler(CannotFollowYourselfException)
    def cannot_follow_yourself_handler(
        request: Request, exc: CannotFollowYourselfException
    ):
        return JSONResponse(
            status_code=400, content={"detail": "Cannot follow yourself"}
        )

    @app.exception_handler(SQLAlchemyError)
    def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Database operation failed. Check your input format/length."
            },
        )

    @app.exception_handler(AlbumNotFoundException)
    def album_not_found_handler(request: Request, exc: AlbumNotFoundException):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(CloudinaryUploadException)
    def cloudinary_upload_handler(request: Request, exc: CloudinaryUploadException):
        return JSONResponse(
            status_code=500, content={"detail": "Failed to upload image"}
        )

    @app.exception_handler(AlreadyLikedException)
    def already_liked_handler(request: Request, exc: AlreadyLikedException):
        return JSONResponse(status_code=409, content={"detail": "Review already liked"})

    @app.exception_handler(LikeNotFoundException)
    def like_not_found_handler(request: Request, exc: LikeNotFoundException):
        return JSONResponse(status_code=404, content={"detail": "Like not found"})
