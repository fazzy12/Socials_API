from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app = FastAPI()

class Post(BaseModel):
    Title: str
    Content: str
    Published: bool = True
    Rating: Optional[int] = None

class updatePost(BaseModel):
    Title: Optional[str] = None
    Content: Optional[str] = None
    Published: Optional[bool] = None
    Rating: Optional[int] = None

# Sample list of dictionaries with 10 items
data_list = [
    {"id": 1, "title": "Item 1", "content": "This is the content of Item 1."},
    {"id": 2, "title": "Item 2", "content": "This is the content of Item 2."},
    {"id": 3, "title": "Item 3", "content": "This is the content of Item 3."},
    {"id": 4, "title": "Item 4", "content": "This is the content of Item 4."},
    {"id": 5, "title": "Item 5", "content": "This is the content of Item 5."},
    {"id": 6, "title": "Item 6", "content": "This is the content of Item 6."},
    {"id": 7, "title": "Item 7", "content": "This is the content of Item 7."},
    {"id": 8, "title": "Item 8", "content": "This is the content of Item 8."},
    {"id": 9, "title": "Item 9", "content": "This is the content of Item 9."},
    {"id": 10, "title": "Item 10", "content": "This is the content of Item 10."},
]


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get('/posts')
def get_post():
    return {'post': data_list}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    data_list.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    for post in data_list:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for post in data_list:
        if post['id'] == post_id:
            data_list.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.put('/posts/{post_id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, updated_post: updatePost):
    for post in data_list:
        if post['id'] == post_id:
            # Update only non-None fields
            for field, value in updated_post.dict(exclude_unset=True).items():
                post[field.lower()] = value
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

