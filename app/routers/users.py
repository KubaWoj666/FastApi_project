from fastapi import APIRouter, Depends, HTTPException, status
from .. import models, schemas, oauth2, utils
from ..database import get_db
from sqlalchemy.orm import Session
import sqlalchemy
from pydantic import EmailStr


router = APIRouter(
    prefix="/users",
    tags=["User"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = utils.hash_password(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_306_RESERVED,
                            detail=f"User with email: {new_user.email} already exist!!")

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user_by_id(id: int, current_user: int = Depends(oauth2.get_concurrent_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} dos not exist!!")
    return user


@router.get("/user/{email}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user_by_email(email: EmailStr, current_user: int = Depends(oauth2.get_concurrent_user),
                      db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email: {email} dos not exist!!")
    return user
