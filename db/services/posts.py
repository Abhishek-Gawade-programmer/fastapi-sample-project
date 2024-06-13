from db.models import Post, User
from db.schemas.posts import PostCreate, PostRead

from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import delete, update


def get_all_user_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.owner_id == user_id).all()


def delete_post_by_id(db: Session, post_id: int):
    post = select(Post).filter(Post.id == post_id)
    db.execute(delete(post))
    db.commit()
    return {"message": "Post deleted"}


def get_post_by_id(db: Session, post_id: int, user_id: int):
    return db.query(Post).filter(Post.id == post_id, Post.owner_id == user_id).first()


def create_post(db: Session, post: PostCreate, user_id: int):
    db_post = Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post_by_id(db: Session, post_id: int):
    delete_post = delete(Post).where(Post.id == post_id)
    db.execute(delete_post)
    db.commit()

    return None
