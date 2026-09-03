from fastapi import APIRouter, Depends
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api/mypage", tags=["mypage"])


@router.get("/bookmarks")
def get_bookmarks(user_id: int = Depends(get_current_user_id)):
    policy_ids = store.bookmarks.get(user_id, set())
    policies = store.load_json("policies.json")
    return [p for p in policies if p["id"] in policy_ids]


@router.get("/chat-history")
def get_chat_history(user_id: int = Depends(get_current_user_id)):
    return store.chat_history.get(user_id, [])


@router.get("/posts")
def get_my_posts(user_id: int = Depends(get_current_user_id)):
    return [p for p in store.posts if p["user_id"] == user_id]
