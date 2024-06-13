from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List


from db.schemas.users import (
    UserOut,
    UserAuth,
    UserCreateDB,
    TokenSchema,
    UserLogin,
    SystemUser,
)

from utils import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)


from core.dependencies import get_db, get_current_user

from sqlalchemy.orm import Session
from db.services import users as user_service

users_router = APIRouter()


# status
@users_router.get("/status")
def status_check():
    return {"status": "ok"}


@users_router.post("/signup", summary="Create new user", response_model=UserOut)
def create_user(data: UserAuth, db: Session = Depends(get_db)):
    # querying database to check if user already exist

    user = user_service.get_user_by_email(db, data.email)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    # hashing password
    hashed_password = get_hashed_password(data.password)
    user = user_service.create_user(
        db, UserCreateDB(email=data.email, password=hashed_password)
    )

    return user


@users_router.post(
    "/login",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
)
def login(form_data: UserLogin, db: Session = Depends(get_db)):

    user = user_service.get_user_by_email(db, form_data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    hashed_pass = user.hashed_password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }


@users_router.get(
    "/me", summary="Get details of currently logged in user", response_model=UserOut
)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user
