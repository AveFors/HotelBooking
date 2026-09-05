from pydantic import BaseModel, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: str
    hashed_password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class UserResponseWithHashPass(UserResponse):
    hashed_password: str
