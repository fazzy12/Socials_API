from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from typing import Optional, List
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, utils


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get('/posts', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    print("Received post data:", post.dict())
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schemas.Post)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return 'done'
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.put('/posts/{post_id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Post)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        post.title = updated_post.title
        post.content = updated_post.content
        post.published = updated_post.published
        db.commit()
        db.refresh(post)
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserView)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    masked_password = utils.hash(user.password)
    user.password = masked_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/users/{user_id}', response_model=schemas.UserView)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User: {user_id} not found")
