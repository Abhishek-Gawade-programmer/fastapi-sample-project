from pydantic import BaseModel, Field, EmailStr


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class UserCreateDB(UserAuth):
    password: str


class UserOut(BaseModel):
    id: int
    email: str


class UserInDB(UserOut):
    password: str


class SystemUser(UserOut):
    password: str
