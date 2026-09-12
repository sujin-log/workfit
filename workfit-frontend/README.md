# 청년워크핏 프론트엔드 (React + Vite)

근로기준법 RAG 기반 AI 노무상담 플랫폼의 사용자 인터페이스

---

## 📋 개발 기획

### 핵심 UI/UX 목표
청년 사용자들이 **직관적이고 친근한 인터페이스**로 법률 정보에 쉽게 접근하도록 설계

### 주요 페이지

| 페이지 | 기능 |
|--------|------|
| **홈 대시보드** | 정책/뉴스 트렌드, 추천 정책, 인기 게시물 |
| **워크챗** | RAG 기반 AI 노무상담 (채팅 UI) |
| **커뮤니티** | 게시글 작성/수정/삭제, 댓글, 좋아요 |
| **정책 검색** | 지역/나이/카테고리별 정책 필터링 |
| **마이페이지** | 북마크, 채팅 이력, 프로필 편집 |
| **인증** | 회원가입, 로그인, 비밀번호 찾기 |

---

## 🛠️ 기술 스택

### Framework & Build
- **React** 19.2.8 - UI 라이브러리
- **Vite** 8.2.2 - 빠른 빌드 도구
- **React Router** 7.18.3 - 클라이언트 라우팅

### HTTP & API
- **Axios** 1.20.0 - HTTP 클라이언트
- **Backend**: FastAPI (localhost:8000)

### UI Components & Styling
- **Recharts** 3.10.1 - 차트 시각화
- **react-markdown** 10.1.0 - Markdown 렌더링
- **CSS Modules** - 컴포넌트별 스타일링

### 개발 도구
- **Oxlint** 1.79.0 - 코드 린팅

---

## ✨ 기대 효과

### 사용자 경험
✅ **직관적 인터페이스**: 청년 맞춤형 디자인
✅ **빠른 응답**: Vite 기반 빠른 로딩 속도
✅ **반응형 디자인**: 모바일/PC 모두 최적화
✅ **친근한 톤**: 법률 정보의 쉬운 이해

### 기술적 장점
✅ **최신 React**: 함수형 컴포넌트 + Hooks
✅ **빠른 개발**: Vite의 빠른 핫 리로드
✅ **라우팅**: React Router v7 기반 SPA
✅ **API 통합**: Axios로 간단한 백엔드 연동

### 사용자 접근성
✅ 24/7 언제든 접근 가능
✅ 별도 앱 설치 불필요 (웹 기반)
✅ 회원가입부터 상담까지 한 플랫폼에서 해결

---

## 📁 프로젝트 구조

```
src/
├── App.jsx                      # 메인 App 컴포넌트
├── main.jsx                     # React 진입점
├── index.css                    # 글로벌 스타일
│
├── api/
│   └── client.js               # Axios API 클라이언트 설정
│
├── components/
│   ├── Auth/
│   │   ├── Auth.jsx            # 로그인/회원가입/비밀번호 찾기
│   │   └── Auth.module.css
│   │
│   ├── Home/
│   │   ├── Home.jsx            # 홈 대시보드
│   │   ├── NewsTrendChart.jsx  # 뉴스 트렌드 차트
│   │   ├── RatioCharts.jsx     # 정책 카테고리 비율
│   │   ├── PolicyCard.jsx      # 추천 정책 카드
│   │   └── HotPost.jsx         # 인기 게시물
│   │
│   ├── Chat/
│   │   ├── Chat.jsx            # 워크챗 페이지 ⭐
│   │   ├── ChatMessage.jsx     # 메시지 컴포넌트
│   │   └── Chat.module.css
│   │
│   ├── Policy/
│   │   ├── Policy.jsx          # 정책 검색 페이지
│   │   ├── PolicyDetail.jsx    # 정책 상세
│   │   └── Policy.module.css
│   │
│   ├── Community/
│   │   ├── Community.jsx       # 커뮤니티 페이지
│   │   ├── PostForm.jsx        # 게시글 작성
│   │   ├── PostList.jsx        # 게시글 목록
│   │   └── Community.module.css
│   │
│   ├── MyPage/
│   │   ├── MyPage.jsx          # 마이페이지
│   │   ├── Bookmarks.jsx       # 북마크
│   │   ├── ChatHistory.jsx     # 채팅 이력
│   │   └── MyPage.module.css
│   │
│   ├── Navigation.jsx          # 네비게이션 바
│   └── Navigation.module.css
│
└── public/
    └── logo.svg               # 로고 (황금색)
```

---

## 🎨 디자인 특징

### 시각적 아이덴티티
- **브랜드 색상**: 보라색 그래디언트 (#667eea → #764ba2)
- **강조 색상**: 황금색 (로고)
- **레이아웃**: 모든 페이지 width 80% 통일

### 반응형 설계
- PC: 전체 기능 제공
- 태블릿: 적응형 레이아웃
- 모바일: 터치 최적화 UI

### 사용자 피드백
- 로딩 상태 표시
- 폼 유효성 검사
- 성공/오류 메시지

---

## 🚀 실행 방법

### 1. 의존성 설치
```bash
npm install
```

### 2. 환경 변수 설정
```bash
cp .env.example .env
# VITE_API_URL=http://localhost:8000
```

### 3. 개발 서버 실행
```bash
npm run dev
```

**접속**: http://localhost:5173

### 4. 프로덕션 빌드
```bash
npm run build
```

빌드 결과: `dist/` 폴더

---

## 📱 주요 페이지 설명

### 1. 홈 대시보드
- 뉴스 트렌드 차트 (시계열 시각화)
- 정책 카테고리 비율
- 추천 정책 (상위 2개)
- 인기 게시물 (상위 3개)

### 2. 워크챗 ⭐
```
사용자 입력: "퇴사 후 임금을 안 줬어요"
    ↓
RAG 검색 + Gemini 답변
    ↓
표시 내용:
  - AI 답변 (자연스러운 톤)
  - 근거 조문 (Top-5)
  - 법령 출처 및 링크
```

### 3. 커뮤니티
- 게시글 목록 (최신순/인기순)
- 게시글 작성 (마크다운 지원)
- 댓글 기능
- 좋아요 기능

### 4. 정책 검색
- 지역 필터링
- 나이대 필터링
- 카테고리 필터링
- 정렬 (마감임박순/최신순)
- 북마크 추가/제거

### 5. 마이페이지
- 북마크 목록 조회
- 채팅 이력 조회
- 내 게시글 조회
- 프로필 편집 (이름, 생년도)

---

## 🔗 백엔드 연동

### API 클라이언트 (`api/client.js`)
```javascript
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

// 요청마다 JWT 토큰 자동 추가
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 주요 엔드포인트
- `POST /api/chat` - 워크챗 (RAG 검색 + 답변)
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `GET /api/policy/search` - 정책 검색
- `GET /api/community/posts` - 게시글 목록
- `POST /api/community/posts` - 게시글 작성
- `GET /api/mypage/bookmarks` - 북마크 조회
- `POST /api/policy/{id}/bookmark` - 북마크 추가

---

## 📊 성능 지표

| 항목 | 값 |
|------|-----|
| 번들 크기 | <500KB (gzipped) |
| 초기 로딩 | <2초 |
| 상호작용 시간 | <100ms |

---

## 🔮 향후 개선

### Phase 1: 사용자 경험
- [ ] 다크모드 지원
- [ ] 웹 푸시 알림
- [ ] 오프라인 캐싱

### Phase 2: 기능 확장
- [ ] 검색 결과 자동 완성
- [ ] 게시글 카테고리 추가
- [ ] 유저 팔로우 기능

### Phase 3: 성능 최적화
- [ ] 코드 스플리팅
- [ ] 이미지 최적화
- [ ] 캐시 전략 개선

---

## 📚 참고

- [React 문서](https://react.dev)
- [Vite 문서](https://vitejs.dev)
- [React Router 문서](https://reactrouter.com)

---

**마지막 업데이트**: 2026-09-12
