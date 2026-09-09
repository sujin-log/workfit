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

### 워크챗 (Chat)
- ✅ 질문 & 답변 (`POST /api/chat`)
- ✅ 관련 법조항 추출
- ✅ Claude API 통합 (선택사항)
- ✅ 더미 답변 (API 키 없을 때)
- ✅ 채팅 이력 (`GET /api/chat/history`)

### 마이페이지 (MyPage)
- ✅ 북마크 목록 (`GET /api/mypage/bookmarks`)
- ✅ 채팅 이력 (`GET /api/mypage/chat-history`)
- ✅ 내 게시글 (`GET /api/mypage/posts`)

### 뉴스 (News)
- ✅ 뉴스 목록 (더미데이터)
- ✅ 뉴스 트렌드

---

## ❌ 아직 미구현 기능

### 외부 API 연동
- ❌ BigKinds API (뉴스 수집)
- ❌ Claude API (워크챗 실제 답변 - 선택사항)

### 데이터베이스
- ❌ PostgreSQL 연동 (현재 메모리 저장소)

---

## 🚀 실행 방법

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정 (선택)

```bash
cp .env.example .env
# .env 파일을 열어서 ANTHROPIC_API_KEY 채우기 (없어도 정상 동작)
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
```
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.2
python-jose[cryptography]==3.3.0
passlib==1.7.4
bcrypt==4.0.1
python-multipart==0.0.9
python-dotenv==1.0.1
httpx==0.27.2
sqlmodel==0.0.14
psycopg2-binary==2.9.9
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
- [ ] ANTHROPIC_API_KEY 설정 (워크챗용)
- [ ] BigKinds API 키 발급 및 설정
- [ ] 환경 변수 (.env) 설정
- [ ] 에러 핸들링 강화
- [ ] 로깅 설정

---

## ⚠️ 알려진 제한사항

1. **메모리 저장소**: 서버 재시작 시 모든 데이터 초기화
2. **더미데이터**: BigKinds, 온통청년 API 미연동 (JSON 사용)
3. **워크챗**: Claude API 키 없으면 더미 답변
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

### Phase 1 (높은 우선순위)
- [ ] PostgreSQL 데이터베이스 완성
- [ ] Claude API 워크챗 테스트

### Phase 2 (중간 우선순위)
- [ ] BigKinds API 연동
- [ ] 데이터 검증 강화

### Phase 3 (낮은 우선순위)
- [ ] 캐싱 (Redis)
- [ ] 로깅 시스템
- [ ] 배치 작업 (뉴스 수집)

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

**마지막 업데이트**: 2026-09-10
