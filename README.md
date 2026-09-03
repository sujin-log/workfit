# Youth-Work-Fit 🎯

청년워크핏 - 청년 정책 추천 플랫폼 (해커톤 프로젝트)

## 📋 프로젝트 개요

**Youth-Work-Fit**은 청년들을 위한 정책 정보와 상담 서비스를 제공하는 통합 플랫폼입니다.

### 주요 기능
- 🔍 **정책 검색**: 지역, 나이, 카테고리별 정책 추천
- 💬 **워크챗**: AI 기반 정책 상담 (Claude API)
- 👥 **커뮤니티**: 청년들 간 경험 공유 및 토론
- 📰 **뉴스 트렌드**: 정책 관련 뉴스 및 감정 분석
- 🔖 **북마크**: 관심 정책 저장

---

## 🏗️ 프로젝트 구조

```
workfit/
├── workfit-backend/          # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py          # FastAPI 애플리케이션
│   │   ├── schemas.py       # 요청/응답 모델
│   │   ├── auth_utils.py    # JWT 인증
│   │   ├── store.py         # 메모리 저장소
│   │   ├── routers/         # API 엔드포인트
│   │   └── mock_data/       # 더미 데이터
│   ├── requirements.txt      # 파이썬 의존성
│   ├── .env.example         # 환경 변수 예시
│   └── README.md            # 백엔드 상세 문서
│
├── workfit-frontend/         # React + Vite 프론트엔드
│   ├── src/                 # 소스 코드
│   ├── public/              # 정적 파일
│   ├── package.json         # NPM 의존성
│   ├── vite.config.js       # Vite 설정
│   ├── .env.example         # 환경 변수 예시
│   └── README.md            # 프론트엔드 상세 문서
│
└── README.md                # 이 파일
```

---

## 🚀 빠른 시작

### 1️⃣ 백엔드 실행

```bash
cd workfit-backend

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (선택)
cp .env.example .env

# 서버 실행
python -m uvicorn app.main:app --reload
```

✅ 성공하면: `http://localhost:8000`

### 2️⃣ 프론트엔드 실행

```bash
cd workfit-frontend

# 의존성 설치
npm install

# 환경 변수 설정 (선택)
cp .env.example .env

# 개발 서버 실행
npm run dev
```

✅ 성공하면: `http://localhost:5173`

---

## 📚 API 문서

### Swagger UI (권장)
```
http://localhost:8000/docs
```
모든 API를 브라우저에서 직접 테스트 가능

### ReDoc
```
http://localhost:8000/redoc
```
API 문서 읽기 전용

---

## 🧪 테스트 계정

```
이메일: test@test.com
비밀번호: password
이름: 테스트유저
나이: 25
```

또는 API를 통해 새로운 계정을 가입할 수 있습니다.

---

## 📖 상세 문서

각 부분에 대한 상세 정보는 다음 문서를 참조하세요:

- [백엔드 문서](./workfit-backend/README.md) - 백엔드 API 구조, 기능 목록, 개발 가이드
- [프론트엔드 문서](./workfit-frontend/README.md) - 프론트엔드 구조, 빌드 및 배포 가이드

---

## 🔧 기술 스택

### Backend
- **FastAPI** 0.115.0 - 모던 Python 웹 프레임워크
- **Uvicorn** - ASGI 서버
- **Pydantic** - 데이터 검증
- **SQLModel** - SQL 데이터베이스 ORM
- **Python-Jose** - JWT 토큰 관리

### Frontend
- **React** 19.2 - UI 라이브러리
- **Vite** - 빌드 도구
- **React Router** - 클라이언트 라우팅
- **Axios** - HTTP 클라이언트
- **Recharts** - 차트 라이브러리

---

## 📊 현재 구현 상태

### ✅ 완료된 기능

**인증**
- 회원가입 / 로그인
- JWT 토큰 기반 인증

**정책**
- 검색 (지역, 나이, 카테고리별 필터)
- 상세 조회
- 북마크

**대시보드**
- 정책 트렌드
- 뉴스 감정 분석
- 추천 정책

**커뮤니티**
- 게시글 작성/수정/삭제
- 댓글 추가
- 좋아요

**워크챗**
- AI 기반 정책 상담
- 채팅 이력 저장

**마이페이지**
- 북마크 목록
- 채팅 이력
- 내 게시글

---

## ⚠️ 현재 제약사항

1. **메모리 저장소**: 서버 재시작 시 모든 데이터 초기화
2. **더미 데이터**: 실제 API 미연동 (JSON 사용)
3. **워크챗**: Claude API 키 없으면 더미 답변
4. **CORS**: 현재 모든 도메인 허용 (배포 시 수정 필수)

---

## 🔐 환경 변수

### 백엔드 (.env)
```
ANTHROPIC_API_KEY=your_api_key_here  # Claude API (선택)
DATABASE_URL=postgresql://...         # DB 연결 (향후)
```

### 프론트엔드 (.env)
```
VITE_API_URL=http://localhost:8000   # 백엔드 API 주소
```

---

## 📞 문제 해결

### 포트 충돌
```bash
# 백엔드 다른 포트로 실행
python -m uvicorn app.main:app --port 8001 --reload

# 프론트엔드 다른 포트로 실행
npm run dev -- --port 5174
```

### 의존성 문제
```bash
# 백엔드
pip install --upgrade -r requirements.txt

# 프론트엔드
rm -rf node_modules package-lock.json
npm install
```

---

## 🎯 개발 계획

### Phase 1 (높은 우선순위)
- [ ] PostgreSQL 데이터베이스 연동
- [ ] Claude API 워크챗 통합

### Phase 2 (중간 우선순위)
- [ ] BigKinds API (뉴스 수집)
- [ ] 온통청년 API (정책 정보)

### Phase 3 (낮은 우선순위)
- [ ] Redis 캐싱
- [ ] 로깅 시스템
- [ ] 배치 작업 (뉴스 수집)

---

## 📈 최근 업데이트 (2026-09-04)

- ✅ 프론트엔드 중복 파일 정리
- ✅ README 통합
- ✅ 프로젝트 구조 정리

---

## 🤝 기여

이 프로젝트는 해커톤 프로젝트입니다. 문제 사항이나 개선 제안이 있으면 이슈를 등록해주세요.

---

**행운을 빕니다! 🚀**
