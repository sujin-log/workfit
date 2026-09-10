from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
    UpdateProfileRequest,
    UpdateProfileResponse,
)
from app.auth_utils import hash_password, verify_password, create_access_token, get_current_user_id
from app.models import User
from app.database import get_session
from app import store
import uuid
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, session: Session = Depends(get_session)):
    try:
        # DB에서 중복 확인
        existing_user = session.exec(select(User).where(User.email == req.email)).first()
        if existing_user:
            raise ValueError("이미 가입된 이메일입니다.")

        # DB에 새 사용자 저장
        user = User(
            email=req.email,
            password_hash=hash_password(req.password),
            name=req.name,
            age=req.age
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # 메모리에도 동기화 (기존 코드 호환성)
        store.users[user.id] = {
            "id": user.id,
            "email": user.email,
            "password_hash": user.password_hash,
            "name": user.name,
            "age": user.age
        }
        store.users_by_email[user.email] = user.id

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"[회원가입 에러] {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"회원가입 실패: {str(e)}")

    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token, user={"id": user.id, "email": user.email, "name": user.name})


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == req.email)).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    token = create_access_token(user.id, user.email)
    return TokenResponse(access_token=token, user={"id": user.id, "email": user.email, "name": user.name})


@router.get("/me")
def get_me(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return {"id": user.id, "email": user.email, "name": user.name, "age": user.age}


@router.put("/me", response_model=UpdateProfileResponse)
def update_profile(req: UpdateProfileRequest, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """프로필 업데이트 (이름, 나이)"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    user.name = req.name
    user.age = req.age
    session.add(user)
    session.commit()
    session.refresh(user)

    # 메모리에도 동기화
    if user.id in store.users:
        store.users[user.id]["name"] = req.name
        store.users[user.id]["age"] = req.age

    return UpdateProfileResponse(
        message="프로필이 성공적으로 업데이트되었습니다.",
        user={"id": user.id, "email": user.email, "name": user.name, "age": user.age}
    )


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(req: ForgotPasswordRequest, session: Session = Depends(get_session)):
    """비밀번호 재설정 요청"""
    user = session.exec(select(User).where(User.email == req.email)).first()

    if not user:
        raise HTTPException(status_code=404, detail="등록되지 않은 이메일입니다.")

    # 재설정 토큰 생성
    reset_token = str(uuid.uuid4())

    # 메모리에 저장 (실제로는 DB에 저장하고 만료시간 설정)
    if not hasattr(store, "reset_tokens"):
        store.reset_tokens = {}
    store.reset_tokens[reset_token] = {
        "user_id": user.id,
        "email": user.email,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=1),
    }

    return ForgotPasswordResponse(
        message=f"비밀번호 재설정 링크가 {user.email}로 전송되었습니다.",
        reset_token=reset_token,  # 테스트용 (실제 환경에서는 제거)
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(req: ResetPasswordRequest, session: Session = Depends(get_session)):
    """새 비밀번호 설정"""

    # 재설정 토큰 확인
    if not hasattr(store, "reset_tokens") or req.reset_token not in store.reset_tokens:
        raise HTTPException(status_code=400, detail="유효하지 않은 재설정 토큰입니다.")

    token_data = store.reset_tokens[req.reset_token]

    # 토큰 만료 확인
    if datetime.now() > token_data["expires_at"]:
        del store.reset_tokens[req.reset_token]
        raise HTTPException(status_code=400, detail="재설정 토큰이 만료되었습니다.")

    # 사용자 조회
    user = session.get(User, token_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 비밀번호 업데이트
    user.password_hash = hash_password(req.new_password)
    session.add(user)
    session.commit()

    # 사용된 토큰 삭제
    del store.reset_tokens[req.reset_token]

    return ResetPasswordResponse(
        message="비밀번호가 성공적으로 변경되었습니다.",
        success=True,
    )
