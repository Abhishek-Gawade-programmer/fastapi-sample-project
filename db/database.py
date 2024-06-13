import psycopg2
import os
from fastapi import HTTPException
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings


Base = declarative_base()

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def get_db_core_connection():
    return next(_get_db_core())


def _get_db_core():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_connection_cursor():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            cursor_factory=RealDictCursor,
        )
        print("Connection to PostgreSQL DB successful")
        return connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)


def db_create_object(db, new_object):
    db.add(new_object)
    db.commit()
    db.refresh(new_object)

    return new_object


def model_to_dict(model):
    """Convert a SQLAlchemy model to a Python dictionary."""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}
