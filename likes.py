from fastapi import HTTPException, status, APIRouter, Depends

from schemas import (LikeCreatSchema)
from security import pwd_context, get_current_user

import main


likes_router = APIRouter(tags=["Likes API's"])


@likes_router.post("/api/like")
def like(like_create_data: LikeCreatSchema,
         current_user=Depends(get_current_user)):
    try:
        user_id = dict(current_user).get("user_id")

        main.cursor.execute("""INSERT INTO likes (user_id, post_id) VALUES (%s, %s) RETURNING *""",
                            (user_id, like_create_data.post_id))
        main.conn.commit()

        return "ok"

    except Exception as err:
        raise HTTPException(status_code=401, detail=str(err))


@likes_router.delete("/api/like/delete/{id}")
def delete_like(id: int,
                current_user=Depends(get_current_user)):
    try:
        user_id = dict(current_user).get("user_id")

        main.cursor.execute("""SELECT * FROM likes WHERE id=%s""",
                            (id,))

        like = main.cursor.fetchone()

        like_user_id = dict(like).get("user_id")

        if user_id != like_user_id:
            raise HTTPException(status_code=403, detail="can not unlike!")

        main.cursor.execute("""DELETE FROM likes WHERE id=%s RETURNING *""",
                            (id,))
        main.cursor.fetchone()

        main.conn.commit()

        return "ok"

    except Exception as err:
        raise HTTPException(status_code=401, detail=str(err))
