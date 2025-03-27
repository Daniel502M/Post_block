from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from sendemail import send_email
from schemas import UserSignUpSchema, UserLoginSchema
from security import pwd_context, create_access_token
import main


users_auth_router = APIRouter(tags=["User Auth API's"])


@users_auth_router.post("/api/sign-up")
def sign_up(new_user_data: UserSignUpSchema):
    name = new_user_data.name
    email = new_user_data.email
    password = new_user_data.password

    hashed_password = pwd_context.hash(password)

    main.cursor.execute("""INSERT INTO users (name, email, password) VALUES (%s, %s, %s)""",
                        (name, email, hashed_password))
    main.conn.commit()
    send_email(email, "Post!", "I have a best car of the planet!")

    return "OK"


@users_auth_router.post("/api/login")
def login(login_data: UserLoginSchema):
    try:
        email = login_data.email
        password = login_data.password
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        main.cursor.execute("""SELECT * FROM users WHERE email=%s""",
                            (email,))
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        user = main.cursor.fetchone()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email '{email}' was not found!"
        )

    if not pwd_context.verify(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong Password"
        )

    user_info = {"user_id": dict(user).get('id')}
    access_token = create_access_token(user_info)

    return access_token
