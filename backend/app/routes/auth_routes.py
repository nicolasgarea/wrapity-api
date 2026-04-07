from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.user_repositories import UserRepository
from app.schemas.user_schemas import UserLogin, UserRegister
from app.services.auth_services import Auth
from app.schemas.token_schemas import Token
from fastapi import status

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service(db: Session = Depends(get_db)) -> Auth:
    repo = UserRepository(db)
    return Auth(repo)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
def register(
    user_data: UserRegister, auth_service: Auth = Depends(get_auth_service)
) -> Token:
    token = auth_service.register_user(
        user_data.username, user_data.email, user_data.password
    )
    return Token(access_token=token, token_type="bearer")


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        401: {"description": "Invalid credentials"},
        404: {"description": "User not found"},
    },
)
def login(
    user_data: UserLogin, auth_service: Auth = Depends(get_auth_service)
) -> Token:
    token = auth_service.login_user(user_data.email, user_data.password)
    return Token(access_token=token, token_type="bearer")
