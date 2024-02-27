from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix='/login',
    tags=["Authentication"]
)


@router.post('/')
def login(user_cridentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.Users).filter(
        models.Users.email == user_cridentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_cridentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"Token": access_token, "Token type": "bearer"}
