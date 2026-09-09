# Youth-Work-Fit 프론트엔드 (React + Vite)

청년워크핏 프론트엔드입니다. React 19와 Vite를 사용하여 빠르고 효율적인 UI를 제공합니다.

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일 수정:
```
VITE_API_URL=http://localhost:8000
```

### 3. 개발 서버 실행

```bash
npm run dev
```

✅ 성공하면: `http://localhost:5173`

---

## 📁 프로젝트 구조

```
src/
├── App.jsx                    # 메인 App 컴포넌트
├── main.jsx                   # 진입점
├── api/
│   └── client.js             # Axios API 클라이언트
├── components/
│   ├── Auth/
│   │   └── Auth.jsx          # 로그인/회원가입
│   ├── Home/
│   │   ├── Home.jsx          # 홈 대시보드
│   │   ├── NewsTrendChart.jsx# 뉴스 트렌드 차트
│   │   ├── RatioCharts.jsx   # 통계 차트
│   │   ├── PolicyCard.jsx    # 정책 카드
│   │   └── HotPost.jsx       # 인기 게시물
│   ├── Policy/               # 정책 검색 페이지 (작업 중)
│   ├── Community/            # 커뮤니티 페이지 (작업 중)
│   ├── Chat/                 # 워크챗 페이지 (작업 중)
│   └── MyPage/               # 마이페이지 (작업 중)
└── public/                    # 정적 파일
```

---

## 📚 현재 구현된 페이지

### ✅ Auth (인증)
- 로그인
- 회원가입
- JWT 토큰 관리

### ✅ Home (대시보드)
- 📰 뉴스 트렌드 차트
- 📊 정책 카테고리 비율
- 🎯 추천 정책 카드
- 🔥 인기 게시물

---

## ⏳ 작업 중인 페이지

### 🔄 Policy (정책 검색)
**예정 기능**:
- 정책 검색 & 필터링
- 지역별 필터
- 나이별 필터
- 카테고리별 필터
- 정책 상세 페이지
- 북마크 추가/제거

### 🔄 Community (커뮤니티)
**예정 기능**:
- 게시글 목록
- 게시글 작성
- 게시글 수정/삭제
- 댓글 추가
- 좋아요 기능

### 🔄 Chat (워크챗)
**예정 기능**:
- 정책 관련 질문
- AI 기반 답변
- 채팅 이력 조회
- 관련 법조항 표시

### 🔄 MyPage (마이페이지)
**예정 기능**:
- 북마크 목록
- 채팅 이력
- 내 게시글
- 프로필 수정

---

## 🔧 기술 스택

- **React** 19.2.8 - UI 라이브러리
- **Vite** 8.2.2 - 빌드 도구
- **React Router** 7.18.3 - 라우팅
- **Axios** 1.20.0 - HTTP 클라이언트
- **Recharts** 3.10.1 - 차트 라이브러리

### 개발 도구
- **Oxlint** 1.79.0 - 린팅
- **Vite** - HMR 지원

---

## 🛠️ 사용 가능한 스크립트

```bash
# 개발 서버 실행
npm run dev

# 프로덕션 빌드
npm run build

# 빌드 결과 미리보기
npm run preview

# 린팅 (코드 품질 체크)
npm run lint
```

---

## 📡 백엔드 연동

### API 클라이언트 설정

`src/api/client.js`에서 Axios 인스턴스 설정:

```javascript
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});
```

### 인증 (JWT)

로그인 후 받은 `access_token`을 로컬스토리지에 저장:

```javascript
localStorage.setItem('token', response.data.access_token);
```

API 요청 시 헤더에 토큰 추가:

```javascript
headers: {
  'Authorization': `Bearer ${localStorage.getItem('token')}`
}
```

---

## 📋 컴포넌트 개발 가이드

### 새로운 페이지 추가 방법

1. `src/components/` 아래 폴더 생성
   ```bash
   mkdir src/components/NewPage
   ```

2. 컴포넌트 파일 생성
   ```jsx
   // src/components/NewPage/NewPage.jsx
   export default function NewPage() {
     return (
       <div>
         <h1>새로운 페이지</h1>
       </div>
     );
   }
   ```

3. `App.jsx`에서 라우트 추가
   ```jsx
   import NewPage from './components/NewPage/NewPage';
   
   // Route 등록
   <Route path="/newpage" element={<NewPage />} />
   ```

---

## 🔐 환경 변수

```
VITE_API_URL=http://localhost:8000    # 백엔드 API 주소
```

---

## 📞 문제 해결

### 포트 5173 이미 사용 중
```bash
npm run dev -- --port 5174
```

### 의존성 문제
```bash
rm -rf node_modules package-lock.json
npm install
```

### CORS 오류
백엔드의 CORS 설정 확인 (현재 모든 도메인 허용)

### 토큰 만료
로그아웃 후 다시 로그인해주세요.

---

## 🎨 UI/UX 가이드

### 색상 팔레트
프로젝트 내 일관된 색상 사용 (Tailwind CSS 또는 CSS 변수)

### 컴포넌트 재사용
`src/components/` 아래 재사용 가능한 컴포넌트 작성

### 반응형 디자인
모바일, 태블릿, 데스크톱 모두 대응

---

## 📈 다음 개발 순서

1. ✅ Auth 페이지
2. ✅ Home 페이지
3. ⏳ Policy 검색 페이지
4. ⏳ Community 페이지
5. ⏳ WorkChat 페이지
6. ⏳ MyPage 페이지

---

## 🚀 배포

### 프로덕션 빌드
```bash
npm run build
```

빌드 결과는 `dist/` 폴더에 생성됩니다.

### 배포 체크리스트
- [ ] `.env` 프로덕션 설정 확인
- [ ] API_URL 프로덕션 주소로 변경
- [ ] 빌드 성공 확인
- [ ] dist 폴더 배포

---

## 🤝 기여

이 프로젝트는 해커톤 프로젝트입니다.

---

**행운을 빕니다! 🚀**

**마지막 업데이트**: 2026-09-10
