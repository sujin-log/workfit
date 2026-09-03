"""
지금은 DB 없이 파이썬 딕셔너리/리스트로 데이터를 들고 있는 '가짜 DB'.
나중에 SQLModel + PostgreSQL로 교체할 때, 이 파일의 함수들 내부 구현만 바꾸면
라우터 코드는 거의 안 건드려도 되게 설계함.
"""
import json
from pathlib import Path

MOCK_DIR = Path(__file__).parent / "mock_data"


def load_json(filename: str):
    with open(MOCK_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


# ---- 서버 실행 중 유지되는 인메모리 데이터 ----
users: dict[int, dict] = {}          # user_id -> {id, email, password_hash, name, age}
users_by_email: dict[str, int] = {}  # email -> user_id
_next_user_id = 1

bookmarks: dict[int, set[int]] = {}  # user_id -> {policy_id, ...}
chat_history: dict[int, list[dict]] = {}  # user_id -> [{chat_id, question, answer}, ...]
_next_chat_id = 1

posts: list[dict] = [
    {
        "id": 1,
        "user_id": 0,
        "author": "익명청년",
        "title": "3개월차 신입인데 다들 이 시기 힘드셨나요?",
        "content": "적응이 잘 안 되네요...",
        "likes": 12,
        "comments": [],
    }
]
_next_post_id = 2


def create_user(email: str, password_hash: str, name: str, age: int) -> dict:
    global _next_user_id
    if email in users_by_email:
        raise ValueError("이미 가입된 이메일입니다.")
    user = {"id": _next_user_id, "email": email, "password_hash": password_hash, "name": name, "age": age}
    users[_next_user_id] = user
    users_by_email[email] = _next_user_id
    _next_user_id += 1
    return user


def get_user_by_email(email: str) -> dict | None:
    user_id = users_by_email.get(email)
    return users.get(user_id) if user_id else None


def get_user_by_id(user_id: int) -> dict | None:
    return users.get(user_id)


def save_chat(user_id: int, question: str, answer: str) -> int:
    global _next_chat_id
    entry = {"chat_id": _next_chat_id, "question": question, "answer": answer}
    chat_history.setdefault(user_id, []).append(entry)
    _next_chat_id += 1
    return entry["chat_id"]


def add_post(user_id: int, nickname: str, title: str, content: str) -> dict:
    global _next_post_id
    post = {"id": _next_post_id, "user_id": user_id, "author": nickname, "title": title, "content": content, "likes": 0, "comments": []}
    posts.append(post)
    _next_post_id += 1
    return post
