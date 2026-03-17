from pydantic import BaseModel, ConfigDict


class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    bio: str | None = None
    avatar_url: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    bio: str | None = None
    avatar_url: str | None = None
