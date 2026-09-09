from sqlmodel import Session, create_engine, SQLModel, select
from sqlalchemy import text, event
import os
from dotenv import load_dotenv
from pathlib import Path

# .env 파일 명시적 로드
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path, override=True)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./workfit.db")

if "postgresql" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        connect_args={
            "client_encoding": "utf8",
            "connect_timeout": 10,
        }
    )
else:
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def create_db_and_tables():
    # 모델 임포트 (테이블 메타데이터 등록)
    from app.models import User, Bookmark, Post, Comment, ChatHistory

    print(f"📌 DATABASE_URL: {DATABASE_URL}")
    print(f"📌 엔진 타입: {type(engine)}")
    print(f"📌 메타데이터 테이블: {SQLModel.metadata.tables.keys()}")

    try:
        SQLModel.metadata.create_all(engine)
        print("✅ 모든 테이블이 생성되었습니다:")
        print("   - users")
        print("   - bookmarks")
        print("   - posts")
        print("   - comments")
        print("   - chat_histories")
    except Exception as e:
        import traceback
        print(f"⚠️  테이블 생성 실패: {e}")
        print(f"📌 전체 에러:\n{traceback.format_exc()}")


def get_session():
    with Session(engine) as session:
        yield session
