from fastapi import HTTPException, status, APIRouter, Depends

from schemas import (CommentCreateSchema,CommentUpdateSchema)
from security import pwd_context, get_current_user

import main


comments_router = APIRouter(tags=["Comments API's"])


@comments_router.get("/")
def get_comments():
    main.cursor.execute("""SELECT * FROM comments""")

    comments = main.cursor.featchall()

    return comments


@comments_router.post("/api/comments")
def add_comments(data: CommentCreateSchema,
                 current_user=Depends(get_current_user)):
    try:
        user_id = dict(current_user).get("user_id")

        main.cursor.execute("""INSERT INTO comments (user_id, post_id, comment) VALUES (%s, %s, %s) RETURNING *""",
                            (user_id, data.post_id, data.comment))
        main.conn.commit()

        return "ok"

    except Exception as err:
        raise HTTPException(status_code=401, detail=str(err))



@comments_router.put("/api/comments/update")
def update_comment(data: CommentUpdateSchema,
                   current_user=Depends(get_current_user)):
    comment_id = data.comment_id
    new_comment_text = data.comment

    main.cursor.execute("""SELECT * FROM comments WHERE id=%s""",
                        (comment_id,))
    comment = main.cursor.fetchone()

    comment_user_id = dict(comment).get("user_id")

    user_id = dict(current_user).get("user_id")

    if comment_user_id != user_id:
        raise HTTPException(status_code=403, detail="this comment is not your`s")

    main.cursor.execute("""UPDATE comments SET comment=%s WHERE id=%s""",
                        (new_comment_text, comment_id))
    main.conn.commit()

    return "ok"

