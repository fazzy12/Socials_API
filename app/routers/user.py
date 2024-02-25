from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserView)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    masked_password = utils.hash(user.password)
    user.password = masked_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{user_id}', response_model=schemas.UserView)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User: {user_id} not found")
