from typing import Union

from api.v1.endpoints.users import users_router
from api.v1.endpoints.posts import post_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(post_router, prefix="/posts", tags=["posts"])
