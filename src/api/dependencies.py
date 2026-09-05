from typing import Annotated

from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel, Field

from src.services.auth import AuthService


class Pagination(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=5, le=30)


PaginationDep = Annotated[Pagination, Depends()]


def get_access_token(request: Request):
    access_token = request.cookies.get("access_token")
    if access_token is None:
        raise HTTPException(status_code=401, detail="Пользователь не аутентифицирован.")
    return access_token


def get_current_user_id(token: Annotated[str, Depends(get_access_token)]) -> int:
    decode_token = AuthService().decode_token(token)
    return int(decode_token["sub"])


UserIdDep = Annotated[int, Depends(get_current_user_id)]
