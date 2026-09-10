# Youth-Work-Fit

청년워크핏 - 청년 정책 추천 플랫폼 (해커톤 프로젝트)

## 프로젝트 개요

**Youth-Work-Fit**은 청년들을 위한 정책 정보와 상담 서비스를 제공하는 통합 플랫폼입니다.

### 주요 기능

#### 핵심 기능 ⭐
- **워크챗 (RAG 기반 AI 상담)**
  - 근로기준법 132개 조문 검색 (ChromaDB + bge-m3 임베딩)
  - Google Gemini 3.6 Flash로 자연스러운 답변 생성
  - 사용자 질문과 관련 법조항 자동 매칭

#### 기본 기능
- **정책 검색**: 지역, 나이, 카테고리별 (더미 데이터)
- **커뮤니티**: 게시글, 댓글, 좋아요
- **북마크**: 관심 정책 저장 및 조회
- **마이페이지**: 북마크, 채팅 이력, 프로필 관리

#### 향후 확장 예정
- **뉴스 트렌드**: BigKinds API 연동 시 실시간 뉴스 수집
- **감정 분석**: BigKinds API 연동 시 뉴스 감정 분석

---

## 프로젝트 구조

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

## 빠른 시작

### 1. 백엔드 실행

```bash
cd workfit-backend

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정 (선택)
cp .env.example .env

# 서버 실행
python -m uvicorn app.main:app --reload
```

성공하면: `http://localhost:8000`

### 2. 프론트엔드 실행

```bash
cd workfit-frontend

# 의존성 설치
npm install

# 환경 변수 설정 (선택)
cp .env.example .env

# 개발 서버 실행
npm run dev
```

성공하면: `http://localhost:5173`

---

## API 문서

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

## 상세 문서

각 부분에 대한 상세 정보는 다음 문서를 참조하세요:

- [백엔드 문서](./workfit-backend/README.md) - 백엔드 API 구조, 기능 목록, 개발 가이드
- [프론트엔드 문서](./workfit-frontend/README.md) - 프론트엔드 구조, 빌드 및 배포 가이드

---

## 기술 스택

### Backend
- **FastAPI** 0.115.0 - 모던 Python 웹 프레임워크
- **Uvicorn** - ASGI 서버
- **Pydantic** - 데이터 검증
- **Python-Jose** - JWT 토큰 관리

### RAG 파이프라인 (워크챗 핵심)
- **ChromaDB** 0.4.24 - 벡터 DB (법조항 저장)
- **sentence-transformers** (bge-m3) - 한국어 최적화 다국어 임베딩
- **Google Generative AI** 0.8.6 - Gemini 3.6 Flash API
- **National Law API** (open.law.go.kr) - 근로기준법 데이터 소스

### Frontend
- **React** 19.2 - UI 라이브러리
- **Vite** - 빌드 도구
- **React Router** - 클라이언트 라우팅
- **Axios** - HTTP 클라이언트
- **Recharts** - 차트 라이브러리

---

## 현재 구현 상태

### 완료된 기능

**인증**
- 회원가입 / 로그인
- JWT 토큰 기반 인증
- 비밀번호 찾기 (이메일 검증, 1시간 만료 토큰)
- CORS + 환경 변수 설정

**프로필**
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

### UI/UX 개선

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


## 최근 업데이트 (2026-09-11)

**완료된 작업:**
- ✅ Google Gemini API 통합 (워크챗 AI 답변)
- ✅ 워크챗 페이지 UI 통일 (보라색 그래디언트)
- ✅ Markdown 렌더링 (react-markdown)
- ✅ 비밀번호 찾기 (이메일 검증, 토큰 기반 재설정)
- ✅ 프로필 편집 (이름, 생년도 수정)
- ✅ 중복 CSS 제거 (.error-message, .success-message)
- ✅ .env.example 파일 생성 및 API 키 참조 통일
- ✅ UI/UX 개선 (네비게이션, 로고, 정책 검색 레이아웃)
- ✅ 코드 최적화 (공통 스타일 통합)

---

## 현재 제약사항

1. **데이터 저장**: 메모리 기반 (서버 재시작 시 초기화)
   - 사용자, 게시글, 북마크는 메모리 저장 (향후 PostgreSQL 연동)
   
2. **정책 데이터**: 더미 JSON 기반
   - 온통청년 API 사용 안 함 (국가법령정보센터 API로 대체)
   - 추천 정책 기능은 더미 데이터로 제공
   
3. **배포 준비**: CORS 설정, 환경 변수 관리 필요

---

## 환경 변수

각 폴더의 `.env.example` 파일을 참고하여 `.env` 파일을 설정하세요.

- `workfit-backend/.env.example`
- `workfit-frontend/.env.example`

---

## 아직 진행해야 할 작업

### Phase 1: 배포 준비 (높음)
- [ ] PostgreSQL 데이터베이스 연동
- [ ] CORS 설정 정제 (프로덕션 URL 지정)
- [ ] 환경 변수 (.env) 설정 검증
- [ ] 에러 로깅 및 모니터링

### Phase 2: 추가 기능 (중간)
- [ ] **BigKinds API 연동** (뉴스 트렌드, 감정 분석)
- [ ] Redis 캐싱 (성능 최적화)
- [ ] 이메일 SMTP 설정 (비밀번호 재설정)

### Phase 3: 향후 확장 (낮음)
- [ ] 온통청년 API 정책 실시간 연동 (선택사항)
- [ ] 추가 법령 데이터 (근로기준법 외 타 법령)

---

## 기여

이 프로젝트는 해커톤 프로젝트입니다.

---

## 🎯 전체 기능 완성도

| 모듈 | 상태 | 진행률 |
|------|------|--------|
| **인증** (Auth) | ✅ 완료 | 100% |
| **홈 대시보드** (Home) | ✅ 완료 | 100% |
| **정책 검색** (Policy) | ✅ 완료 | 100% |
| **커뮤니티** (Community) | ✅ 완료 | 100% |
| **워크챗** (Chat) | ✅ 완료 | 100% |
| **마이페이지** (MyPage) | ✅ 완료 | 100% |
| **외부 API 연동** | 🔄 진행중 | 50% |

**마지막 업데이트**: 2026-09-11
