from fastapi import FastAPI, Response, status, HTTPException, Request, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

route = APIRouter( prefix= "/users", tags=['users'])

# routes for usersUserResponse
@route.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hash_password = utils.encrypt(user.password)
    user.password = hash_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@route.get("/{id}", response_model= schemas.UserResponse)
def find_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"User with id = {id} does not exist",
                         )
    else: 
        return user