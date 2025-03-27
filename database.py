from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/social_media"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
