# Youth-Work-Fit 청년워크핏

근로기준법 RAG 기반 AI 노무상담 플랫폼

---

## 📋 개발 기획

### 핵심 비전
청년 근로자들이 직면한 **법률 관련 문제를 신뢰할 수 있는 AI 상담**으로 해결하는 통합 플랫폼

### 주요 기능

| 기능 | 설명 |
|------|------|
| **워크챗** | 근로기준법 RAG 기반 AI 노무상담 |
| **정책/뉴스 대시보드** | 청년 정책 및 일자리 트렌드 시각화 |
| **커뮤니티** | 청년들 간 경험 공유 및 토론 |
| **북마크 & 마이페이지** | 관심 정책 저장 및 개인 정보 관리 |

---

## 🛠️ 기술 스택

### Backend
- **Framework**: FastAPI 0.115.0
- **Server**: Uvicorn 0.30.6
- **Authentication**: JWT (python-jose)
- **Data Validation**: Pydantic 2.9.2

### RAG 파이프라인 (워크챗 핵심)
- **Vector DB**: ChromaDB 0.4.24
- **Embedding Model**: BAAI/bge-m3 (한국어 최적화)
- **LLM**: Google Gemini 3.6 Flash (google-generativeai 0.8.6)
- **Data Source**: 국가법령정보센터 API (근로기준법)

### Frontend
- **Framework**: React 19.2.8
- **Build Tool**: Vite 8.2.2
- **Routing**: React Router 7.18.3
- **HTTP Client**: Axios 1.20.0
- **Charts**: Recharts 3.10.1
- **Markdown**: react-markdown 10.1.0

### Storage
- **Users/Posts/Bookmarks**: In-memory (서버 재시작 시 초기화)
- **Dummy Data**: JSON (정책, 뉴스, 통계)

---

## ✨ 기대 효과

### 사용자 관점
✅ **정확한 정보**: 법령 기반의 신뢰할 수 있는 상담
✅ **24/7 접근**: 언제든지 이용 가능한 AI 상담
✅ **비용 절감**: 법률 전문가 상담 비용 없음
✅ **쉬운 이해**: 친근한 톤의 설명

### 기술 관점
✅ **할루시네이션 방지**: RAG로 거짓 정보 생성 차단
✅ **확장성**: 다른 법령 추가 가능한 구조
✅ **신뢰성**: 실제 API 데이터만 사용
✅ **투명성**: 답변의 법령 근거 명시

### 비즈니스 관점
✅ 청년 커뮤니티 플랫폼의 완성도 향상
✅ 사용자 체류 시간 증가 (AI 상담 활용)
✅ 신뢰도 기반 재방문율 증가
✅ 향후 다양한 도메인으로 확장 가능

---

## 🚀 프로젝트 구조

```
workfit/
├── workfit-backend/           # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   │   ├── chat.py          ⭐ RAG 워크챗
│   │   │   ├── community.py
│   │   │   ├── auth.py
│   │   │   └── ...
│   │   └── mock_data/
│   │       └── labor_articles.json  ⭐ 근로기준법 132개 조문
│   ├── scripts/
│   │   ├── fetch_labor_law_real.py
│   │   └── rebuild_chroma_bge_m3.py
│   ├── chroma_db_bge_m3/           ⭐ 벡터 DB (프로덕션)
│   └── requirements.txt
│
└── workfit-frontend/          # React 프론트엔드
    ├── src/
    │   ├── components/
    │   │   ├── Chat/             ⭐ 워크챗 UI
    │   │   ├── Community/
    │   │   ├── MyPage/
    │   │   └── ...
    │   └── api/
    │       └── client.js
    └── package.json
```

---

## 🎯 워크챗 (RAG 노무상담)

### 동작 원리
```
사용자 질문
    ↓
bge-m3 임베딩 + ChromaDB 검색
    ↓
근로기준법 Top-5 조문 추출
    ↓
Gemini 3.6 Flash로 답변 생성
    ↓
법령 최신정보 고지 자동 추가
    ↓
최종 답변 반환
```

### 예시
```
질문: "퇴사 후 임금을 안 줬어요"

검색 결과:
  제36조 (금품청산) - 유사도 60.9% ⭐

답변:
"근로기준법 제36조에 따르면 사장님은 
 퇴사한 날부터 14일 이내에 모든 임금을 지급해야 해..."
```

---

## 📊 성능 지표

| 항목 | 값 |
|------|-----|
| 근로기준법 조문 | 132개 |
| 검색 정확도 (제36조) | 60.9% (1순위) ⭐ |
| 평균 응답 시간 | <1초 |
| 벡터 DB 크기 | 1.4MB |

---

## 🚀 빠른 시작

### 백엔드
```bash
cd workfit-backend
pip install -r requirements.txt
cp .env.example .env
# .env에 GOOGLE_API_KEY 입력
python -m uvicorn app.main:app --reload
```

**접속**: http://localhost:8000/docs

### 프론트엔드
```bash
cd workfit-frontend
npm install
cp .env.example .env
npm run dev
```

**접속**: http://localhost:5173

---

## 🔮 향후 계획

### Phase 1: 배포 준비
- PostgreSQL 데이터베이스 연동
- CORS 설정 정제
- 모니터링 & 로깅

### Phase 2: 기능 확장
- BigKinds API (뉴스 데이터)
- 정기 데이터 재수집 자동화
- 추가 법령 확대 (근로기준법 외)

### Phase 3: 성능 최적화
- Redis 캐싱
- 응답 시간 개선

---

## 📚 상세 문서

- [백엔드 문서](./workfit-backend/README.md) - RAG 구현, API 명세
- [프론트엔드 문서](./workfit-frontend/README.md) - UI/UX, 컴포넌트 구조

---

**마지막 업데이트**: 2026-09-12
