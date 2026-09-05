from fastapi import APIRouter, HTTPException, Response, Body

from typing import Annotated

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth")


@router.post("/register", summary="Регистрация")
async def register(
    user: Annotated[
        UserRequestAdd,
        Body(
            openapi_examples={
                "1": {
                    "summary": "Иванов Иван Иваныч",
                    "value": {
                        "email": "ivanov@blabla.com",
                        "password": "ivanchik2003",
                    },
                }
            }
        ),
    ],
):
    hashed_password = AuthService().hash_password(user.password)
    new_hashed_user = UserAdd(
        email=user.email,
        hashed_password=hashed_password,
    )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_hashed_user)
        await session.commit()
        return {"status": "OK"}


@router.post("/login", summary="Логин")
async def login(
    user: Annotated[UserRequestAdd, Body()],
    response: Response,
):
    async with async_session_maker() as session:
        db_user = await UsersRepository(session).get_user_with_hash_password(
            email=user.email
        )
        if not db_user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегестрирован."
            )
        if not AuthService().verify_password(
            plain_password=user.password, hashed_password=db_user.hashed_password
        ):
            raise HTTPException(status_code=401, detail="Неверный email или пароль.")
        access_token = AuthService().create_access_token(data={"sub": str(db_user.id)})
        response.set_cookie(
            "access_token",
            access_token,
            httponly=True,
            secure=True,
            samesite="lax",
        )
        return {"access_token": access_token}


@router.post("/logout", summary="Выход")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
