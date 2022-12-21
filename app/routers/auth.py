from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    tags=['Authentication']
)


@router.post("/login/")
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """OAuth2PasswordRequestForm returns something like thad
        {"username": "example username,
         "password: "example password} " so we have to change user_credential.email in to
        user_credential.username"""
    """Also we have to change our testing way in postman (screen nr1) """
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")

    if not utils.veryfi_password(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "Bearer"}

