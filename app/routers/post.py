from fastapi import FastAPI, Response, status, HTTPException, Request, Depends, APIRouter
from .. import models, schemas, oauth2
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

route = APIRouter(prefix= "/posts", tags=['posts'])

#  response_model= List[schemas.PostOut]
@route.get('/', response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db), current_user: schemas.TokenPayload = Depends(oauth2.get_current_user),
    page_limit: int = 10, skip: int = 0, search: Optional[str] = "" ):
    # cursor.execute("SELECT * FROM posts;")
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(page_limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(page_limit).offset(skip).all()
    return posts

# @route.get('/', response_model= List[schemas.Post])
# def get_posts_by_user(db: Session = Depends(get_db), current_user: schemas.TokenPayload = Depends(oauth2.get_current_user)):
#     # cursor.execute("SELECT * FROM posts;")
#     posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
#     return posts

@route.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.PostCreateResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, description) VALUES(%s, %s) RETURNING *",(post.title, post.description))
    # savedPost = cursor.fetchone()
    # conn.commit()
    new_post= models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
 
@route.get("/{id}", response_model=schemas.PostOut)
def find_post_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.TokenPayload = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('likes')).join(
        models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= f"Post with id = {id} does not exist",
                         )
    return post

@route.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.TokenPayload = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (id,))
    # post = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"Post with id: {id} does not exist"
        )
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to perform this action")
    query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@route.put("/{id}", response_model= schemas.PostCreateResponse)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, description = %s WHERE id = %s RETURNING *", (post.title, post.description, id,))
    # updatedPost = cursor.fetchone()
    query = db.query(models.Post).filter(models.Post.id == id)
    old_post = query.first()
    if old_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail= f"Post with id = {id} does not exist")

    if old_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="You are not authorized to perform this action")
    query.update(post.dict(), synchronize_session= False)
    db.commit()
    return query.first()
