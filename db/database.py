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
