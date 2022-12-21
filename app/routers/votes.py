from fastapi import APIRouter, Depends, HTTPException, status, Response
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Votes, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_concurrent_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} dos not exist!")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User with id: {current_user.id} already voted on post id: {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"massage": "successful added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="vote not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"massage": "Successful delete vot!"}

