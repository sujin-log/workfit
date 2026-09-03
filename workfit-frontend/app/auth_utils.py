"""
JWT 발급/검증 + 비밀번호 해싱 유틸.
실제 운영에서는 SECRET_KEY를 .env로 빼야 함 (지금은 해커톤용으로 하드코딩).
"""
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Header

SECRET_KEY = "hackathon-dev-secret-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24시간

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, email: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user_id(authorization: str = Header(None)) -> int:
    """
    요청 헤더의 'Authorization: Bearer <token>'을 검증해서 user_id를 꺼내주는 함수.
    라우터에서 Depends(get_current_user_id)로 붙이면 로그인 필요한 API에 바로 쓸 수 있음.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")
