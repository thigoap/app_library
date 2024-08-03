from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserPatch(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class AuthorSchema(BaseModel):
    name: str


class AuthorPublic(AuthorSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AuthorUpdate(BaseModel):
    name: str | None = None


class AuthorList(BaseModel):
    authors: list[AuthorPublic]
