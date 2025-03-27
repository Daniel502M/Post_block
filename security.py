from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/login")

TOKEN_SECRET_KEY = "@s_im_tokeny_sekret_keyna,vore_vochmek_chpiti_imana!"
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
