from fastapi import HTTPException, status, APIRouter

from schemas import (UsernameChangeSchema, PasswordChangeSchema)
from security import pwd_context

# from main import conn, cursor
import main


users_router = APIRouter(tags=["User API's"])

# =============================== User APIs ==================================

@users_router.get("/api/get/users")
def get_all_users():
    try:
        main.cursor.execute("""SELECT * FROM users""")
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    try:
        users = main.cursor.fetchall()
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err)
        )

    return users


@users_router.get("/api/get/users/{id}")
def get_user_by_id(id: int):
    main.cursor.execute("""SELECT * FROM users WHERE id=%s""",
                   (id,))
    user = main.cursor.fetchone()

    return user


@users_router.put("/api/users/change/name/{id}")
def change_username(id: int, username_change_data: UsernameChangeSchema):
    main.cursor.execute("""UPDATE users SET name=%s WHERE id=%s""",
                        (username_change_data.name, id))
    main.conn.commit()

    return "OK"


@users_router.put("/api/users/change/password/{id}")
def change_password(id: int, password_change_data: PasswordChangeSchema):
    password = password_change_data.password
    new_password = password_change_data.new_password

    main.cursor.execute("""SELECT password FROM users WHERE id=%s""",
                   (id,))
    user = main.cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    hashed_password = pwd_context.hash(new_password)

    main.cursor.execute("""UPDATE users SET password=%s WHERE id=%s""",
                   (hashed_password, id))
    main.conn.commit()

    return "OK"


@users_router.delete("/api/users/delete/account/{id}")
def delete_user_account(id: int):
    main.cursor.execute("""DELETE FROM users WHERE id=%s RETURNING *""",
                        (id,))
    main.cursor.fetchone()

    main.conn.commit()
    return "OK"
