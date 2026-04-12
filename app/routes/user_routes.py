from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.clients.cloudinary_client import CloudinaryClient
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repositories import UserRepository
from app.schemas.user_schemas import UserResponse, UserUpdate
from app.services.user_services import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    client = CloudinaryClient()
    return UserService(repo, client)


@router.get(
    "/me",
    response_model=UserResponse,
    responses={401: {"description": "Not authenticated"}},
)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return current_user


@router.patch(
    "/me",
    response_model=UserResponse,
    responses={401: {"description": "Not authenticated"}},
)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    updated_user = user_service.update_user(
        current_user, user_update.username, user_update.bio, user_update.avatar_url
    )
    return updated_user


@router.post(
    "/me/avatar",
    response_model=UserResponse,
    responses={
        401: {"description": "Not authenticated"},
        500: {"description": "Upload failed"},
    },
)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    content = await file.read()
    return user_service.upload_avatar(current_user, content)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    responses={404: {"description": "Not found"}},
)
def get_user_by_id(
    user_id: int, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    user = user_service.get_user_by_id(user_id)
    return user
