# from fastapi.params import Body
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# generate tables
# models.Base.metadata.create_all(bind = engine)

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app is a decorator. its a way from which they modify the behaviour of function.
@app.get('/')
def root():
    return { "message": "Hello, from Aditya" }

app.include_router(post.route)
app.include_router(user.route)
app.include_router(auth.route)
app.include_router(vote.route)