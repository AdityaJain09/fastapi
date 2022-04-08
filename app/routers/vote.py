from fastapi import FastAPI, Response, status, HTTPException, Request, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import Vote

route = APIRouter(prefix="/vote", tags=['vote'])

@route.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} Doesn't exist.")

    query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    old_vote = query.first()
    # there is one error that if different users trying to like same post then it shows error
    if vote.likes:
        if old_vote != None:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
            detail=f"User with {current_user.id} already Liked the post {vote.post_id}")
        new_post = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_post)
        db.commit()
        return { "status": "Post Liked Successfully"}
    else:
        if old_vote == None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail=f"Post Does not exist")
    query.delete(synchronize_session=False)
    db.commit()
    return { "status": "Post Liked Removed Successfully."}

    # , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
 