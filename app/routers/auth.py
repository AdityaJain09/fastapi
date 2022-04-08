from fastapi import FastAPI, Response, status, HTTPException, Request, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, oauth2
from .. import utils

route = APIRouter(
    tags=['Authentication']
    )

@route.post("/login", response_model= schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    access_token  = oauth2.create_token(payload = {"user_id": user.id})
    return { "access_token": access_token, "token_type": "bearer"}
