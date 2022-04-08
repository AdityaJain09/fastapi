from jose import JWTError, jwt
from fastapi.security.oauth2 import OAuth2PasswordBearer
from datetime import datetime, timedelta
from . import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from .config import settings

oauth2_scheme = OAuth2PasswordBearer("login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_DAYS = settings.access_token_expire_days

def create_token(payload: dict):
    encode_data = payload.copy()

    expire_time = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    encode_data.update({ "exp": expire_time})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise credential_exception
        token_data = schemas.TokenPayload(id = id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),  db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"Could not authroized credentials.",
                                         headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
