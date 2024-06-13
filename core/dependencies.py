from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from db.services import users as user_service
from sqlalchemy.orm import Session
from utils import ALGORITHM, JWT_SECRET_KEY

from jose import jwt
from pydantic import ValidationError
from db.schemas.users import TokenPayload, SystemUser

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

Base = declarative_base()

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="users/login", scheme_name="JWT")


token_auth_scheme = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized request",
        )

    token_data = TokenPayload(**payload)
    email: str = token_data.sub
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = user_service.get_user_by_email(db, email)

    return user
