from fastapi import APIRouter, Depends, File, UploadFile
import shutil
import os
import uuid

from schemas import PostCreateSchema, PostUpdateSchema
from security import pwd_context, get_current_user


# from main import conn, cursor
import main

UPLOAD_DIR = "C:\Photo_Python\Photo_API`s"
os.makedirs(UPLOAD_DIR, exist_ok=True)

posts_router = APIRouter(tags=["Post API's"])

# =============================== Post APIs ==================================


# TODO: Chi asxatum >>>
# @posts_router.post("/api/posts")
# def create_post(new_post_data: PostCreateSchema,
#                 file: UploadFile = File(None),
#                 current_user=Depends(get_current_user)):
#     user_id = dict(current_user).get("user_id")
#
#     image_path = None
#     if file:
#         file_extension = file.filename.split(".")[-1]  # Получаем расширение файла
#         unique_filename = f"{uuid.uuid4()}.{file_extension}"  # Генерируем уникальное имя
#         image_path = os.path.join(UPLOAD_DIR, unique_filename)  # Полный путь к файлу
#
#         with open(image_path, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)  # Сохраняем файл на сервере
#
#     # Записываем в базу данных
#     main.cursor.execute(
#         """INSERT INTO posts (title, content, image, user_id)
#            VALUES (%s, %s, %s, %s) RETURNING id, title, content, image, user_id, created_at""",
#         (new_post_data.title, new_post_data.content, image_path, user_id)
#     )
#     new_post = main.cursor.fetchone()
#     main.conn.commit()
#
#     return {
#         "id": new_post[0],
#         "title": new_post[1],
#         "content": new_post[2],
#         "image": f"/uploads/{os.path.basename(new_post[3])}" if new_post[3] else None,
#         "user_id": new_post[4],
#         "created_at": new_post[5]
#     }
# TODO: Chi ashxatum <<<


@posts_router.post("/api/posts")
def create_post(new_post_data: PostCreateSchema,
                current_user=Depends(get_current_user)):
    user_id = dict(current_user).get("user_id")
    main.cursor.execute(
        """INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s) RETURNING *""",
        (new_post_data.title, new_post_data.content, user_id)
    )
    new_post = main.cursor.fetchone()
    main.conn.commit()

    return new_post


@posts_router.get("/api/get/posts")
def get_all_posts():
    main.cursor.execute("""SELECT * FROM posts""")
    posts = main.cursor.fetchall()

    return posts


@posts_router.get("/api/get/posts/{id}")
def get_post_by_id(id: int):
    main.cursor.execute("""SELECT * FROM posts WHERE id=%s""",
                        (id,))
    post = main.cursor.fetchone()

    return post


@posts_router.get("/api/get/posts/user/{user_id}")
def get_one_user_all_posts(user_id: int):
    main.cursor.execute("""SELECT * FROM posts WHERE user_id=%s""",
                        (user_id,))
    posts = main.cursor.fetchall()

    return posts


@posts_router.put("/api/posts/update/{id}")
def change_post(id: int, post_update_data: PostUpdateSchema):
    main.cursor.execute(
        """UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *""",
        (post_update_data.title, post_update_data.content, id)
    )
    updated_post = main.cursor.fetchone()

    main.conn.commit()

    return updated_post


@posts_router.delete("/api/posts/delete/{post_id}")
def delete_post_by_id(post_id: int):
    main.cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",
                        (post_id,))
    main.cursor.fetchone()

    main.conn.commit()

    return "OK"
