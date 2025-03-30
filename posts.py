from fastapi import APIRouter, Depends, File, UploadFile, Form
from fastapi.responses import FileResponse
import shutil
import os
import uuid

from schemas import PostCreateSchema, PostUpdateSchema
from security import pwd_context, get_current_user

# from main import conn, cursor
import main


UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создаёт папку, если её нет


posts_router = APIRouter(tags=["Post API's"])

# =============================== Post APIs ==================================


@posts_router.post("/api/posts")
def create_post(title: str = Form(...), content: str = Form(...), image: UploadFile = File(...),
                current_user=Depends(get_current_user)):
    user_id = dict(current_user).get("user_id")
    ext = os.path.splitext(image.filename)[-1].lower()  # Получаем расширение файла
    unique_filename = f"{uuid.uuid4()}{ext}"  # Генерируем уникальное имя
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_src = unique_filename
    main.cursor.execute(
        """INSERT INTO posts (title, content, user_id, image_src) VALUES (%s, %s, %s, %s) RETURNING *""",
        (title, content, user_id, image_src)
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


@posts_router.get("/download/{filename}")
def get_photo(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return {"error": "Файл не найден"}

    return FileResponse(file_path)
