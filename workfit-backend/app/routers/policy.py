from fastapi import APIRouter, HTTPException, Depends
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api/policy", tags=["policy"])


@router.get("/search")
def search(region: str | None = None, age: int | None = None, category: str | None = None, sort: str = "deadline"):
    # TODO: 온통청년 인증키 발급되면 youthPlcyList.do 호출로 교체
    policies = store.load_json("policies.json")
    if region:
        policies = [p for p in policies if p["region"] == region]
    if age:
        policies = [p for p in policies if p["min_age"] <= age <= p["max_age"]]
    if category:
        policies = [p for p in policies if p["category"] == category]
    if sort == "deadline":
        policies = sorted(policies, key=lambda p: p["deadline"])
    elif sort == "latest":
        policies = sorted(policies, key=lambda p: p["id"], reverse=True)
    return {"total": len(policies), "policies": policies}


@router.get("/{policy_id}")
def get_detail(policy_id: int):
    policies = store.load_json("policies.json")
    for p in policies:
        if p["id"] == policy_id:
            return p
    raise HTTPException(status_code=404, detail="정책을 찾을 수 없습니다.")


@router.post("/{policy_id}/bookmark")
def add_bookmark(policy_id: int, user_id: int = Depends(get_current_user_id)):
    store.bookmarks.setdefault(user_id, set()).add(policy_id)
    return {"message": "북마크 등록됨", "policy_id": policy_id}


@router.delete("/{policy_id}/bookmark")
def remove_bookmark(policy_id: int, user_id: int = Depends(get_current_user_id)):
    store.bookmarks.get(user_id, set()).discard(policy_id)
    return {"message": "북마크 해제됨", "policy_id": policy_id}
