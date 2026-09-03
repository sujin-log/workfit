from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routers import auth, home, news, policy, chat, community, mypage
from app import store
from app.auth_utils import hash_password

load_dotenv()

app = FastAPI(title="청년워크핏 API", version="0.1.0")

# 테스트 계정 생성
if "test@test.com" not in store.users_by_email:
    store.create_user("test@test.com", hash_password("password"), "테스트유저", 25)

# React 개발 서버(보통 localhost:3000 또는 5173)에서 오는 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 해커톤용 - 배포 시에는 실제 프론트 주소로 제한 권장
    allow_methods=["*"],
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
