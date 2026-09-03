"""
Pydantic 모델 = Java의 DTO 클래스랑 같은 역할.
요청/응답 JSON의 '모양'을 여기서 정의하면 FastAPI가 자동으로 검증 + 직렬화까지 해줌.
"""
from pydantic import BaseModel
from typing import Optional


# ---------- 인증 ----------
class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    age: int


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ---------- 워크챗 ----------
class ChatRequest(BaseModel):
    question: str


class Source(BaseModel):
    law: str
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    chat_id: int


# ---------- 커뮤니티 ----------
class PostCreateRequest(BaseModel):
    title: str
    content: str


class CommentCreateRequest(BaseModel):
    content: str
