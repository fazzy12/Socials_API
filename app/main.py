from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='socialsapi',
                                user='postgres',
                                password='virgin123',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Created connection to database')
        break
    except Exception as e:
        print('Error: ', e)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get('/posts')
def get_post(db: Session = Depends(get_db)):
    posts = db.querry(models.Post).all
    return {'post': posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    post_dict = post.dict()
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    cursor.execute("""
        SELECT * FROM posts WHERE id = %s
    """, (str(post_id),))
    post = cursor.fetchone()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("""
        DELETE FROM posts WHERE id = %s
    RETURNING * """, (str(post_id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{post_id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, updated_post: Post):
    try:
        cursor.execute("""
            UPDATE posts
            SET title = %s, content = %s, published = %s
            WHERE id = %s
            RETURNING *
        """, (updated_post.title, updated_post.content, updated_post.published, post_id))
        conn.commit()

        post = cursor.fetchone()

        if post:
            return post
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))