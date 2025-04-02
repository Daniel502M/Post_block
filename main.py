import time

# Non-Standard libs
from fastapi import FastAPI

import psycopg2
from psycopg2.extras import RealDictCursor

# My libs
from database import engine
from models import Base

from users import users_router
from user_auth import users_auth_router
from posts import posts_router
from comments import comments_router
from likes import likes_router


Base.metadata.create_all(bind=engine)


while True:
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            user='postgres',
            password='password',
            database="social_media",
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("Database connection successfully...")
        break
    except Exception as err:
        print("Couldn't connect to database...")
        print(str(err))
        time.sleep(3)


app = FastAPI()


@app.get("/")
def main():
    return "OK"


app.include_router(users_auth_router)
# app.include_router(users_router)
# app.include_router(posts_router)
# app.include_router(comments_router)
# app.include_router(likes_router)
