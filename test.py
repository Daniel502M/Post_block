import datetime
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

import psycopg2
from psycopg2.extras import RealDictCursor

from pydantic import BaseModel, EmailStr

from sqlalchemy import (
    create_engine, Column, String,
    Integer, TIMESTAMP, text, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base

from passlib.context import CryptContext

from jose import jwt, JWTError

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login")

TOKEN_SECRET_KEY = "dsfvghcfhggbmfhthjhuui45n67t^&T^&T^&^&TGB^&C&^T #G&B#&BG^R"
TOKEN_EXPIRE_MINUTES = 15
TOKEN_ALGORITHM = "HS256"


def create_access_token(user_info: dict):
    expire_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    user_info['exp'] = expire_time

    token = jwt.encode(user_info, TOKEN_SECRET_KEY, algorithm=TOKEN_ALGORITHM)

    return token


def verify_access_token(token: str):
    payload = jwt.decode(token, TOKEN_SECRET_KEY, algorithms=[TOKEN_ALGORITHM])

    return payload


def get_current_user(token=Depends(oauth2_schema)):
    payload = verify_access_token(token)

    return payload


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password='password',
    database="usersdb",
    cursor_factory=RealDictCursor
)

cursor = conn.cursor()


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost:5432/usersdb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("now()"))

    user_id = Column(Integer, ForeignKey("users.id"))


Base.metadata.create_all(bind=engine)


class UserSignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserChangeUsername(BaseModel):
    name: str

class PasswordChangeSchema(BaseModel):
    password: str

class PostCreateSchema(BaseModel):
    posts: str

class PostUpdateSchema(BaseModel):
    post: str

app = FastAPI()


# =============================== User APIs ==================================

@app.post("/api/sign-up")
def sign_up(new_user_data: UserSignUpSchema):
    name = new_user_data.name
    email = new_user_data.email
    password = new_user_data.password

    hashed_password = pwd_context.hash(password)

    cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
                   (name, email, hashed_password))
    conn.commit()

    return "OK"


@app.post("/api/login")
def login(login_data: UserLoginSchema):
    email = login_data.email
    password = login_data.password

    cursor.execute("""SELECT * FROM users WHERE email=%s""",
                   (email,))

    user = cursor.fetchone()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' was not found!"
        )

    if not pwd_context.verify(password, dict(user).get("password")):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Wrong Password '{password}'"
        )

    user_info = {"user_id": dict(user).get('id')}
    access_token = create_access_token(user_info)

    return access_token


@app.get("/api/users")
def get_all_users(current_user=Depends(get_current_user)):
    cursor.execute("""SELECT * FROM users""")

    all_users = cursor.fetchall()

    return all_users


@app.get("/api/users/{id}")
def get_user_by_id(id: int):
    cursor.execute = (""""SELECT * FROM users WHERE id=%s""")

    user = cursor.fetchone
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found"
        )

    return "Ok"


@app.put("/users/change-username/{id}")
def change_username(id: int, username_change: UserChangeUsername):
    new_username = username_change.new_username

    cursor.execute("""UPDATE users SET username=%s WHERE id=%s""",
                   (new_username, id))
    conn.commit()

    return  "OK"



@app.put("/api/users/change/password/{id}")
def change_password(id: int, password_change_data: PasswordChangeSchema):
    new_password = change_password.new_password

    cursor.execute = (""""UPDATE password SET password=%s""",
                      (new_password))

    return "Ok"





# =============================== Post APIs ==================================
# CRUD -> Create, Read, Update, Delete
@app.post("/api/posts/{user_id}")
def create_post(user_id: int, new_post_data: PostCreateSchema):
    new_post = Post(
        title=new_post_data.title,
        content=new_post_data.content
    )
        #created_at=timestamp()<<<<<<<<erora talm>>>>>>>

    return  "Post is sucefuly"


@app.get("/api/posts")
def get_all_posts():
    cursor.execute = ("""SELECT * FROM posts=%s""")

    all_posts = cursor.fetchall


@app.get("/api/posts/{id}")  # id is a post id
def get_post_by_id(id: int):
    cursor.execute = (""""SELECT * FROM posts WHERE id=%s""")

    user = cursor.fetchone
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Posts not found"
        )

    return "Ok"


@app.get("/api/posts/{user_id}") #TODO :::Es chhaskaca:::
def get_one_user_all_posts(user_id: int):
    pass


@app.put("/api/posts/update/{id}")
def change_post(post_update_data: PostUpdateSchema):
    new_post = post_update_data.new_post

    cursor.execute("""UPDATE post SET post=%s WHERE id=%s""",
                   (new_post, id))
    conn.commit()

    return  "OK"
