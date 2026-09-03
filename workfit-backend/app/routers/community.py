from fastapi import APIRouter, HTTPException, Depends
from app.schemas import PostCreateRequest, CommentCreateRequest
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api/community", tags=["community"])


@router.get("/posts")
def list_posts(sort: str = "popular"):
    posts = store.posts
    if sort == "popular":
        posts = sorted(posts, key=lambda p: p["likes"], reverse=True)
    else:
        posts = sorted(posts, key=lambda p: p["id"], reverse=True)
    return posts


@router.post("/posts")
def create_post(req: PostCreateRequest, user_id: int = Depends(get_current_user_id)):
    nickname = store.users[user_id]["name"]
    return store.add_post(user_id, nickname, req.title, req.content)


@router.get("/posts/{post_id}")
def get_post(post_id: int):
    for p in store.posts:
        if p["id"] == post_id:
            return p
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")


@router.put("/posts/{post_id}")
def update_post(post_id: int, req: PostCreateRequest, user_id: int = Depends(get_current_user_id)):
    for p in store.posts:
        if p["id"] == post_id:
            if p["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="본인 글만 수정할 수 있습니다.")
            p["title"], p["content"] = req.title, req.content
            return p
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, user_id: int = Depends(get_current_user_id)):
    for i, p in enumerate(store.posts):
        if p["id"] == post_id:
            if p["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="본인 글만 삭제할 수 있습니다.")
            store.posts.pop(i)
            return {"message": "삭제됨"}
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")


@router.post("/posts/{post_id}/comments")
def add_comment(post_id: int, req: CommentCreateRequest, user_id: int = Depends(get_current_user_id)):
    for p in store.posts:
        if p["id"] == post_id:
            nickname = store.users[user_id]["name"]
            p["comments"].append({"author": nickname, "content": req.content})
            return p
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")


@router.post("/posts/{post_id}/like")
def like_post(post_id: int):
    for p in store.posts:
        if p["id"] == post_id:
            p["likes"] += 1
            return {"likes": p["likes"]}
    raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
