from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    email = Column(String, nullable =  False, unique = True)
    password = Column(String, nullable= False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = True, server_default=text('now()'))

    user_posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False)
    title = Column(String, nullable = False)
    description = Column(String, nullable = False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = True, server_default=text('now()'))

    owner = relationship("User", back_populates="user_posts")

class Vote(Base):
    __tablename__ = "votes"
    post_id = Column(Integer, ForeignKey("posts.id", ondelete= "CASCADE"), primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete= "CASCADE"), primary_key = True)
