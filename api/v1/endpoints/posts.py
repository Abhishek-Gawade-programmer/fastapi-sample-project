from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.dependencies import get_db, get_current_user
from db.schemas.posts import PostCreate, PostRead
from db.services import posts as post_service
from sqlalchemy.orm import Session

post_router = APIRouter()
from cachetools import cached
from cachetools import TTLCache


@post_router.get("/status")
def status_check():
    return {"status": "ok"}


#   AddPost Endpoint:
#     Accepts `text` and a `token` for authentication.
#     Validates payload size (limit to 1 MB), saves the post in memory, returning `postID`.
#     Returns an error for invalid or missing token.


@post_router.post("/add")
def add_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    #  Validates payload size (limit to 1 MB), saves the post in memor
    if len(post.text) > 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post text is too long",
        )
    post = post_service.create_post(db, post, user.id)
    return {"postID": post.id}


@cached(cache=TTLCache(maxsize=1024, ttl=300))  # 5 mins
@post_router.get("/all")
def get_all_user_posts(
    user: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    posts = post_service.get_all_user_posts(db, user.id)
    return posts


@post_router.delete("/delete")
def delete_post(
    post_id: int = Query(...),
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user),
):
    post = post_service.get_post_by_id(db, post_id, user.id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    post_service.delete_post_by_id(db, post_id)
    return {"message": "Post deleted"}
