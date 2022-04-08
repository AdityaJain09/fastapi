from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# users schema

class CreateUser(BaseModel):
    id: int = None
    name: str
    email: EmailStr
    password: str

class UserResponse(CreateUser):
    created_at: datetime
    
    class Config:
        fields = { 'password' : { 'exclude': True}}
        orm_mode = True

class UserAuthentication(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    id: Optional[str] = None

class UserPost(UserResponse):
    class Config:
        fields = { "created_at": { "exclude" : True}}

class PostBase(BaseModel):
    title: str
    description: str

class Post(PostBase):
    id: int
    user_id: int
    created_at: datetime
    owner: UserPost

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    likes: int
    # class Config:
    #     orm_mode= True

class CreatePost(PostBase):
    pass

class PostCreateResponse(PostBase):
    class Config:
        orm_mode = True

# vote schema
class Vote(BaseModel):
    post_id: int
    likes: bool