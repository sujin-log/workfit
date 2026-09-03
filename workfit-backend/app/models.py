from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: str
    age: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Bookmark(SQLModel, table=True):
    __tablename__ = "bookmarks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    policy_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    author: str
    title: str
    content: str
    likes: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Comment(SQLModel, table=True):
    __tablename__ = "comments"

    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="posts.id")
    author: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatHistory(SQLModel, table=True):
    __tablename__ = "chat_histories"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    question: str
    answer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
