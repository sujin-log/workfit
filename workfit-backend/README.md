# 청년워크핏 백엔드 (FastAPI)

더미데이터로 동작하는 실행 가능한 백엔드입니다. 실제 API 키가 없어도 전체 기능을 테스트할 수 있습니다.

## ✅ 현재 구현된 기능

### 인증 (Authentication)
- ✅ 회원가입 (`POST /api/auth/register`)
- ✅ 로그인 (`POST /api/auth/login`)
- ✅ 사용자 정보 조회 (`GET /api/auth/me`)
- ✅ JWT 토큰 기반 인증
- ✅ 비밀번호 찾기 (이메일 검증, 토큰 기반 재설정)
- ✅ 프로필 수정 (이름, 생년도)

### HOME 대시보드
- ✅ 뉴스 트렌드 데이터 (`GET /api/home/summary`)
- ✅ 정책 카테고리 비율
- ✅ 뉴스 감정 분석 (긍정/중립/부정)
- ✅ 추천 정책
- ✅ 인기 게시물

### 정책 (Policy)
- ✅ 정책 검색 (`GET /api/policy/search`)
  - 지역별 필터링
  - 나이별 필터링
  - 카테고리별 필터링
  - 정렬: 마감임박순 ⏰
  - 정렬: 최신순 ⭐ (추가됨)
- ✅ 정책 상세 조회 (`GET /api/policy/{policy_id}`)
- ✅ 북마크 추가 (`POST /api/policy/{policy_id}/bookmark`)
- ✅ 북마크 삭제 (`DELETE /api/policy/{policy_id}/bookmark`)

### 커뮤니티 (Community)
- ✅ 게시글 목록 (`GET /api/community/posts`)
- ✅ 게시글 작성 (`POST /api/community/posts`)
- ✅ 게시글 상세 (`GET /api/community/posts/{post_id}`)
- ✅ 게시글 수정 (`PUT /api/community/posts/{post_id}`)
- ✅ 게시글 삭제 (`DELETE /api/community/posts/{post_id}`)
- ✅ 댓글 추가 (`POST /api/community/posts/{post_id}/comments`)
- ✅ 좋아요 (`POST /api/community/posts/{post_id}/like`)

### 워크챗 (Chat) - RAG 파이프라인
- ✅ **RAG 기반 검색** (`POST /api/chat`)
  - 근로기준법 132개 조문 의미 기반 검색 (ChromaDB + bge-m3)
  - Top-5 관련 조문 자동 추출
- ✅ **Google Gemini 3.6 Flash 통합**
  - 자연스러운 대화형 답변 생성
  - 마크다운 제거 후 일반 텍스트 응답
- ✅ 폴백 검색 (ChromaDB 실패 시 키워드 매칭)
- ✅ 채팅 이력 (`GET /api/chat/history`)

### 마이페이지 (MyPage)
- ✅ 북마크 목록 (`GET /api/mypage/bookmarks`)
- ✅ 채팅 이력 (`GET /api/mypage/chat-history`)
- ✅ 내 게시글 (`GET /api/mypage/posts`)

### 뉴스 (News)
- ✅ 뉴스 목록 (더미데이터)
- ✅ 뉴스 트렌드

---

## 📋 프로젝트 범위 및 구현 상태

### 이번 프로젝트에 포함된 기능
✅ **근로기준법 RAG 파이프라인** (핵심)
  - 국가법령정보센터 API에서 132개 조문 수집
  - ChromaDB + bge-m3 임베딩으로 의미 기반 검색
  - Gemini 3.6 Flash로 자연스러운 답변 생성

✅ 기본 정책/커뮤니티 기능 (더미 데이터)

### 추후 연동 예정
🔄 **BigKinds API** (뉴스 트렌드, 감정 분석)
  - 현재: 더미 JSON 사용 (news_trend.json)
  - 향후: 실시간 뉴스 수집 및 감정 분석 기능 추가 예정

### 사용하지 않는 기능
❌ **온통청년 API** (국가법령정보센터 API로 완전히 대체)

### 데이터베이스
- 현재: 인메모리 저장소 (서버 재시작 시 초기화)
- 향후: PostgreSQL 연동 예정

---

## 🚀 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정 (선택)

```bash
cp .env.example .env
# .env 파일을 열어서 GOOGLE_API_KEY 채우기 (없어도 더미 답변으로 정상 동작)
```

### 3. 서버 실행

```bash
python -m uvicorn app.main:app --reload
```

✅ 성공하면:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 📚 API 테스트

### Swagger UI (권장)
```
http://localhost:8000/docs
```
- 모든 API를 브라우저에서 직접 테스트 가능
- 요청/응답 예시 표시

### ReDoc (대안)
```
http://localhost:8000/redoc
```
- API 문서 읽기 전용

---

## 📁 폴더 구조

```
app/
├── main.py                  # FastAPI 진입점, 라우터 등록
├── schemas.py              # Pydantic 요청/응답 모델 (DTO)
├── store.py                # 인메모리 임시 저장소
├── auth_utils.py           # JWT 발급/검증, 비밀번호 해싱
├── database.py             # DB 연결 (향후 사용)
├── models.py               # SQLModel 정의 (향후 사용)
├── mock_data/              # 더미 JSON 데이터
│   ├── policies.json       # 정책 데이터
│   ├── news_list.json      # 뉴스 목록
│   ├── news_trend.json     # 뉴스 트렌드
│   ├── ratios.json         # 통계 데이터
│   └── law_articles.json   # 법 조항 (워크챗용)
└── routers/                # API 라우터
    ├── auth.py             # 인증 (회원가입, 로그인)
    ├── home.py             # HOME 대시보드
    ├── policy.py           # 정책 검색 & 북마크
    ├── community.py        # 커뮤니티 (글, 댓글)
    ├── chat.py             # 워크챗 (AI 상담)
    ├── mypage.py           # 마이페이지
    └── news.py             # 뉴스
```

---

## 📊 데이터 저장 방식

### 현재 상태
| 항목 | 저장소 | 상태 |
|------|--------|------|
| 사용자 | 메모리 | 서버 재시작 시 초기화 ⚠️ |
| 정책 | JSON (mock_data) | 고정 데이터 |
| 게시글 | 메모리 | 서버 재시작 시 초기화 ⚠️ |
| 북마크 | 메모리 | 서버 재시작 시 초기화 ⚠️ |
| 뉴스 | JSON (mock_data) | 고정 데이터 |

### 향후 계획
- ✅ store.py 구조 (라우터 코드 수정 최소화)
- ❌ SQLModel + PostgreSQL 연동 예정

---

## 🧪 테스트 계정

```
이메일: test@test.com
비밀번호: password
이름: 테스트유저
나이: 25
```

또는 API를 통해 새로 가입할 수 있습니다.

---

## 🔐 인증 방식

### JWT 토큰
```
Authorization: Bearer {token}
```

### 토큰 발급
```bash
POST /api/auth/register
{
  "email": "user@example.com",
  "password": "password123",
  "name": "홍길동",
  "age": 25
}

응답:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "홍길동"
  }
}
```

### 토큰 검증
```bash
GET /api/auth/me
Authorization: Bearer {token}
```

---

## 🔧 개발 환경

### 필수
- Python 3.10+
- pip

### 설치된 패키지

**Core Framework**
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.2
python-jose[cryptography]==3.3.0
passlib==1.7.4
bcrypt==4.0.1
python-multipart==0.0.9
python-dotenv==1.0.1
```

**RAG 파이프라인 (워크챗)**
```
google-generativeai==0.3.0 (⚠️ 버전 불일치 - 실제 사용 중: 0.8.6)
chromadb==0.4.24
sentence-transformers==2.3.1
langchain==0.1.17
PyPDF2==3.0.1
```

---

## 📝 API 엔드포인트 요약

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/auth/me` - 내 정보

### 대시보드
- `GET /api/home/summary` - 홈 대시보드

### 정책
- `GET /api/policy/search?region=&age=&category=&sort=` - 정책 검색
- `GET /api/policy/{policy_id}` - 정책 상세
- `POST /api/policy/{policy_id}/bookmark` - 북마크 추가
- `DELETE /api/policy/{policy_id}/bookmark` - 북마크 제거

### 커뮤니티
- `GET /api/community/posts?sort=` - 글 목록
- `POST /api/community/posts` - 글 작성
- `GET /api/community/posts/{post_id}` - 글 상세
- `PUT /api/community/posts/{post_id}` - 글 수정
- `DELETE /api/community/posts/{post_id}` - 글 삭제
- `POST /api/community/posts/{post_id}/comments` - 댓글 추가
- `POST /api/community/posts/{post_id}/like` - 좋아요

### 워크챗
- `POST /api/chat` - 질문 & 답변
- `GET /api/chat/history` - 채팅 이력

### 마이페이지
- `GET /api/mypage/bookmarks` - 북마크 목록
- `GET /api/mypage/chat-history` - 채팅 이력
- `GET /api/mypage/posts` - 내 게시글

---

## 🚀 배포 체크리스트

배포 전 필수 작업:
- [ ] PostgreSQL 데이터베이스 연동
- [ ] CORS 설정 수정 (프로덕션 URL로 제한)
- [ ] SECRET_KEY 보안 강화 (.env로 이동)
- [ ] GOOGLE_API_KEY 설정 (워크챗용)
- [ ] BigKinds API 키 발급 및 설정
- [ ] 환경 변수 (.env) 설정
- [ ] 에러 핸들링 강화
- [ ] 로깅 설정

---

## ⚠️ 알려진 제한사항

1. **메모리 저장소**: 서버 재시작 시 모든 데이터 초기화
2. **더미데이터**: BigKinds, 온통청년 API 미연동 (JSON 사용)
3. **워크챗**: Google Gemini API 키 없으면 더미 답변
4. **CORS**: 현재 모든 도메인 허용 (배포 시 수정 필수)

---

## 📞 문제 해결

### uvicorn: command not found
```bash
python -m uvicorn app.main:app --reload
```

### 포트 8000 이미 사용 중
```bash
python -m uvicorn app.main:app --port 8001 --reload
```

### 모듈 임포트 에러
```bash
pip install -r requirements.txt
```

### 데이터베이스 에러 (PostgreSQL)
- 현재 메모리 저장소 사용 (에러 무시)
- PostgreSQL 나중에 연동 예정

---

## 📈 다음 개발 계획

### Phase 1: 배포 준비 (높은 우선순위)
- [ ] PostgreSQL 데이터베이스 연동
- [ ] CORS 설정 정제 (프로덕션 URL 지정)
- [ ] 환경 변수 (.env) 설정 검증
- [ ] requirements.txt 버전 정확화 (google-generativeai 0.3.0 → 0.8.6)
- [ ] 에러 로깅 및 모니터링 강화

### Phase 2: 추가 기능 (중간 우선순위)
- [ ] **BigKinds API 연동** (뉴스 트렌드, 감정 분석)
- [ ] Redis 캐싱 (성능 최적화)
- [ ] 이메일 SMTP 설정 (비밀번호 재설정)
- [ ] 데이터 검증 강화

### Phase 3: 향후 확장 (낮은 우선순위)
- [ ] 온통청년 API 정책 실시간 연동 (선택사항)
- [ ] 추가 법령 데이터 (근로기준법 외 타 법령)
- [ ] 캐싱 (Redis)
- [ ] 로깅 시스템 개선

---

## 📅 법령 개정 대비 기능

### 현재 구현된 기능
✅ **수집일자 메타데이터**
  - ChromaDB 저장 시 각 조문에 수집일자 기록
  - 워크챗 답변 끝에 "본 답변은 [수집일자] 기준"이라고 자동 표시

✅ **법령 최신 정보 고지**
  - 답변 끝에 "최신 정보는 국가법령정보센터(law.go.kr)에서 확인하실 수 있습니다" 안내 문구 자동 추가

### 향후 개선 사항: 정기 재수집 자동화
법령이 개정될 수 있으므로, 정기적으로 최신 데이터를 수집하는 자동화가 필요합니다.

**권장 구현 방식:**

1. **Celery + Redis 기반 스케줄러**
   ```python
   # 매주 월요일 새벽 2시에 자동 실행
   from celery.schedules import crontab
   from celery import shared_task
   
   @shared_task
   def scheduled_rebuild_chroma():
       # rebuild_chroma_bge_m3.py의 rebuild_chroma_with_bge_m3() 실행
       from scripts.rebuild_chroma_bge_m3 import rebuild_chroma_with_bge_m3
       rebuild_chroma_with_bge_m3()
   
   app.conf.beat_schedule = {
       'rebuild-chroma-weekly': {
           'task': 'app.tasks.scheduled_rebuild_chroma',
           'schedule': crontab(hour=2, minute=0, day_of_week=1),
       },
   }
   ```

2. **APScheduler 기반 (더 간단)**
   ```python
   from apscheduler.schedulers.background import BackgroundScheduler
   from apscheduler.triggers.cron import CronTrigger
   
   scheduler = BackgroundScheduler()
   scheduler.add_job(
       func=rebuild_chroma_with_bge_m3,
       trigger=CronTrigger(hour=2, minute=0, day_of_week='mon'),
       id='rebuild_chroma',
       name='Weekly ChromaDB Rebuild',
       replace_existing=True
   )
   scheduler.start()
   ```

3. **GitHub Actions (배포 환경에서)**
   - Cron 워크플로우로 정기적으로 데이터 재수집
   - rebuild_chroma_bge_m3.py 실행
   - 새로운 chroma_db_bge_m3 커밋 및 푸시

**우선순위:** Phase 2 또는 Phase 3 (배포 후 추가)

---

## 🎉 시작하기

```bash
# 1. 백엔드 실행
python -m uvicorn app.main:app --reload

# 2. 브라우저에서 API 테스트
http://localhost:8000/docs

# 3. 프론트엔드와 연동
# (workfit-frontend 참조)
```

**행운을 빕니다! 🚀**

---

**마지막 업데이트**: 2026-09-11

## 최근 변경사항 (2026-09-11)

**완료된 작업:**
- ✅ Google Gemini API 통합 (gemini-3.6-flash 모델)
- ✅ 워크챗 Markdown 형식 제거 (자연스러운 문장 답변)
- ✅ 비밀번호 찾기 토큰 기반 재설정
- ✅ 프로필 수정 (이름, 생년도)
- ✅ JWT 기반 인증 강화
- ✅ .env.example 파일 생성
