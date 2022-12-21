from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/comment",
    tags=["Comments"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def create_comment(comment: schemas.Comment, current_user: int = Depends(oauth2.get_concurrent_user),
                   db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {comment.post_id} dos not exist!")

    new_comment = models.Comments(user_id=current_user.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UpdateComment)
def update_comment(id: int, update_comment: schemas.UpdateComment,
                   current_user: int = Depends(oauth2.get_concurrent_user),
                   db: Session = Depends(get_db)):

    comment_query = db.query(models.Comments).filter(models.Comments.comment_id == id)
    comment_to_update = comment_query.first()

    if not comment_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} dos not exist!")

    if comment_to_update.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize")

    comment_query.update(update_comment.dict(), synchronize_session=False)
    db.commit()
    return update_comment


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id:int, current_user: int = Depends(oauth2.get_concurrent_user), db: Session = Depends(get_db)):
    comment_query = db.query(models.Comments).filter(models.Comments.comment_id == id)
    comment_to_delete = comment_query.first()

    if not comment_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} dos not exist!")
    if comment_to_delete.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorize")

    db.delete(comment_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

