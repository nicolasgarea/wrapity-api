from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    bio: str | None = None
    avatar_url: str | None = None
    role: str


class UserUpdate(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    bio: str | None = Field(None, max_length=300)
    avatar_url: str | None = None
