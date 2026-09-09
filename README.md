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

**인증 (Task 1-2)**
- 회원가입 / 로그인
- JWT 토큰 기반 인증
- 비밀번호 찾기 (이메일 검증, 1시간 만료 토큰)
- CORS + 환경 변수 설정

**프로필 (Task 3)**
- 프로필 수정 (이름, 생년도)
- 마이페이지에서 편집 모드

**정책 검색**
- 필터링 (지역, 나이, 카테고리, 정렬)
- 검색 / 초기화 버튼
- 개선된 UI (80% 너비, 필터 확대)
- 개선된 카드 디자인 (흰색 배경, 보라색 테두리)

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
- 프로필 편집

### 🎨 UI/UX 개선

**네비게이션**
- 보라색 그래디언트 배경 (#667eea → #764ba2)
- 커스텀 SVG 로고 (황금색)
- 향상된 호버 효과

**전체 페이지**
- 모든 페이지 width 80%로 통일
- 반응형 디자인 개선
- 공통 스타일 최적화

**코드 최적화**
- index.css에 공통 스타일 통합
- 중복 CSS 제거 (error-message, success-message)
- 불필요한 패턴 정리

---


## 📈 최근 업데이트 (2026-09-10)

**완료된 작업:**
- ✅ Task 2: 비밀번호 찾기 (이메일 검증, 토큰 기반 재설정)
- ✅ Task 3: 프로필 편집 (이름, 생년도 수정)
- ✅ UI/UX 대폭 개선 (네비게이션, 로고, 정책 검색 레이아웃)
- ✅ 코드 최적화 (공통 스타일 통합, 중복 제거)
- ✅ SQLite 파일 제거 (PostgreSQL로 통일)

---

## ⚠️ 현재 제약사항

1. **워크챗**: Claude API 키 없으면 더미 답변
2. **이메일 발송**: 현재 비밀번호 재설정 토큰만 메모리에 저장 (실제 이메일 미발송)
3. **배포 준비**: CORS 설정 정제 필요

---

## 🔐 환경 변수

각 폴더의 `.env.example` 파일을 참고하여 `.env` 파일을 설정하세요.

- `workfit-backend/.env.example`
- `workfit-frontend/.env.example`

---

## 📋 아직 진행해야 할 작업

### Task 4: 배포 준비 ⏳
- [ ] CORS 설정 정제 (프로덕션 도메인 지정)
- [ ] 환경별 설정 분리 (개발/프로덕션)
- [ ] 프로덕션 빌드 테스트
- [ ] 에러 로깅 개선

### 추가 기능 (우선순위 낮음)
- [ ] Claude API 연동 (워크챗 실제 답변)
- [ ] 이메일 SMTP 설정 (비밀번호 재설정 이메일)
- [ ] 정책 API 실제 데이터 연동
- [ ] 뉴스 트렌드 API 연동
- [ ] Redis 캐싱 (성능 최적화)
- [ ] 로깅 시스템 구축

---

## 🤝 기여

이 프로젝트는 해커톤 프로젝트입니다.

---

