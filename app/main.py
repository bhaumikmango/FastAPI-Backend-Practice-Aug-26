from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None

while True:    
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'password123', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('DB connection successful')
        break
    except Exception as e:
        print(e)
        time.sleep(2)

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/latest")
def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    post = cursor.fetchone()
    return {"last post": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Created New Post": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s ORDER BY created_at DESC LIMIT 1""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    a = cursor.fetchone()
    if a == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} doesn\'t exist')
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    conn.commit()
    return {'Post Updated Successfully':updated_post}