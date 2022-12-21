from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


@router.get("/", response_model=List[schemas.PostsOut])
def get_posts(current_user: int = Depends(oauth2.get_concurrent_user), db: Session = Depends(get_db)):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("likes"), models.Comments.comment)\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .join(models.Comments, models.Post.id == models.Comments.post_id, isouter=True)\
        .group_by(models.Post.id, models.Comments.comment).all()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no posts!!")

    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostsOut)
def get_post_by_id(id: int, current_user: int = Depends(oauth2.get_concurrent_user), db: Session = Depends(get_db)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes"), models.Comments.comment) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .join(models.Comments, models.Post.id == models.Comments.post_id, isouter=True) \
        .group_by(models.Post.id, models.Comments.comment).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} das not exist !!")

    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, current_user: int = Depends(oauth2.get_concurrent_user),
                db: Session = Depends(get_db)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, current_user: int = Depends(oauth2.get_concurrent_user), db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    post = delete_post.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} das not exist !!")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No authorize!!")
    delete_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostCreate)
def update_post(id:int, update_post: schemas.PostCreate, current_user: int = Depends(oauth2.get_concurrent_user), db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} das not exist !!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No authorize!!")

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return update_post
