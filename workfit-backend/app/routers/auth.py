from fastapi import APIRouter, HTTPException, Depends
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.auth_utils import hash_password, verify_password, create_access_token, get_current_user_id
from app import store

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest):
    try:
        user = store.create_user(req.email, hash_password(req.password), req.name, req.age)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token = create_access_token(user["id"], user["email"])
    return TokenResponse(access_token=token, user={"id": user["id"], "email": user["email"], "name": user["name"]})


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = store.get_user_by_email(req.email)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    token = create_access_token(user["id"], user["email"])
    return TokenResponse(access_token=token, user={"id": user["id"], "email": user["email"], "name": user["name"]})


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user_id)):
    user = store.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"id": user["id"], "email": user["email"], "name": user["name"], "age": user["age"]}
