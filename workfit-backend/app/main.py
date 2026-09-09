from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routers import auth, home, news, policy, chat, community, mypage
from app import store
from app.auth_utils import hash_password
from app.database import create_db_and_tables

load_dotenv()

app = FastAPI(title="청년워크핏 API", version="0.1.0")

# CORS 설정 (.env에서 읽기)
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# 프로덕션 환경에서는 특정 도메인만 허용
if ENVIRONMENT == "production":
    ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]
else:
    # 개발 환경에서는 모든 로컬호스트 허용
    ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]

@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
        print("✅ 데이터베이스 테이블 생성 완료")
    except Exception as e:
        print(f"⚠️  테이블 생성 실패 (메모리 저장소 사용): {e}")

# 테스트 계정 생성
if "test@test.com" not in store.users_by_email:
    store.create_user("test@test.com", hash_password("password"), "테스트유저", 25)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(news.router)
app.include_router(policy.router)
app.include_router(chat.router)
app.include_router(community.router)
app.include_router(mypage.router)


@app.get("/")
def root():
    return {"message": "청년워크핏 API 서버 동작 중. /docs 에서 API 문서 확인 가능"}
