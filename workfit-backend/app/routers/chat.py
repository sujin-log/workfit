import os
import json
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse, Source
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api", tags=["chat"])


def search_procedures(question: str) -> list[dict]:
    """질문과 관련된 행정 절차 검색"""
    try:
        MOCK_DIR = Path(__file__).parent.parent / "mock_data"
        with open(MOCK_DIR / "procedures.json", encoding="utf-8") as f:
            procedures = json.load(f)

        # 간단한 키워드 매칭으로 관련 절차 검색
        keywords = question.lower().split()
        matched = []

        for proc in procedures:
            title_lower = proc.get("title", "").lower()
            content_lower = " ".join(str(v).lower() for v in proc.values())

            score = sum(1 for kw in keywords if kw in title_lower or kw in content_lower)
            if score > 0:
                matched.append((score, proc))

        matched.sort(key=lambda x: x[0], reverse=True)
        return [proc for _, proc in matched[:1]]  # 가장 관련있는 1개만
    except Exception as e:
        print(f"절차 검색 오류: {e}")
        return []


def search_labor_law_rag(question: str, top_k: int = 5) -> list[dict]:
    """ChromaDB를 사용한 의미 기반 근로기준법 검색 (RAG + bge-m3 임베딩)"""
    try:
        import chromadb
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

        # ChromaDB 경로 (bge-m3 임베딩 사용)
        db_path = Path(__file__).parent.parent.parent / "chroma_db_bge_m3"

        if not db_path.exists():
            # ChromaDB 없으면 더미 검색으로 폴백
            return search_related_articles_fallback(question, top_k)

        # ChromaDB 클라이언트 연결 (bge-m3 임베딩)
        client = chromadb.PersistentClient(path=str(db_path))
        embedding_function = SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-m3"
        )

        collection = client.get_collection(
            name="labor_law",
            embedding_function=embedding_function
        )

        # 질문으로 유사 조문 검색
        results = collection.query(
            query_texts=[question],
            n_results=top_k
        )

        # 검색 결과를 Source 형식으로 변환 (메타데이터 보강)
        articles = []
        if results and results['documents']:
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                law_name = metadata.get('law_name', '근로기준법')
                clause = metadata.get('clause', '?')
                paragraph = metadata.get('paragraph', '')

                # "근로기준법 제36조" 또는 "근로기준법 제36조 제1항" 형태
                law_ref = f"{law_name} 제{clause}조"
                if paragraph:
                    law_ref += f" {paragraph}"

                articles.append({
                    "law": law_ref,
                    "content": doc,
                    "text": doc,
                    "metadata": metadata
                })

        return articles or search_related_articles_fallback(question, top_k)

    except Exception as e:
        print(f"RAG 검색 오류: {e}")
        return search_related_articles_fallback(question, top_k)


def search_related_articles_fallback(question: str, top_k: int = 2) -> list[dict]:
    """폴백: 키워드 기반 조항 검색"""
    articles = store.load_json("law_articles.json")

    # 간단한 키워드 매칭
    scored = []
    keywords = question.split()

    for a in articles:
        content = a.get("text", "").lower()
        score = sum(1 for kw in keywords if kw.lower() in content)
        if score > 0:
            scored.append((score, a))

    scored.sort(key=lambda x: x[0], reverse=True)
    articles = [a for _, a in scored[:top_k]] or articles[:1]

    # Source 형식으로 변환
    return [
        {
            "law": f"제{a.get('clause', '?')}조",
            "content": a.get("content", a.get("text", "")),
            "text": a.get("text", "")
        }
        for a in articles
    ]


def get_collection_date() -> str:
    """ChromaDB 메타데이터에서 수집일자 조회"""
    try:
        import chromadb
        from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

        db_path = Path(__file__).parent.parent.parent / "chroma_db_bge_m3"
        if not db_path.exists():
            return datetime.now().strftime("%Y-%m-%d")

        client = chromadb.PersistentClient(path=str(db_path))
        embedding_function = SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-m3")
        collection = client.get_collection(name="labor_law", embedding_function=embedding_function)

        # 임의의 항목에서 수집일자 조회
        items = collection.get(limit=1)
        if items and items['metadatas'] and len(items['metadatas']) > 0:
            return items['metadatas'][0].get('collection_date', datetime.now().strftime("%Y-%m-%d"))

        return datetime.now().strftime("%Y-%m-%d")
    except:
        return datetime.now().strftime("%Y-%m-%d")


def generate_answer(question: str, related_articles: list[dict], procedure_info: dict = None) -> str:
    """Google Gemini API를 사용한 답변 생성 (실무 기반, 절차 정보 포함)"""
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
        return f"Google Gemini API 키가 설정되지 않았습니다.\n\n관련 법 근거:\n{context}"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.6-flash")

        # 법 조항 컨텍스트
        law_context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)

        # 절차 정보 컨텍스트 (있으면)
        procedure_context = ""
        if procedure_info:
            steps_text = "\n".join([
                f"[{s['step']}단계] {s['name']}\n   신청처: {s['agency']}\n   신청 방법: {s['method']}\n   필요 서류: {', '.join(s['documents']) if s['documents'] else 'N/A'}\n   소요 기간: {s['duration']}\n   비용: {s['cost']}"
                for s in procedure_info.get("steps", [])
            ])
            procedure_context = f"\n\n행정 절차:\n{steps_text}"
            if "penalty_for_nonpayment" in procedure_info:
                procedure_context += f"\n\n불이행 시 조치:\n  법: {procedure_info['penalty_for_nonpayment'].get('law', 'N/A')}\n  처벌: {procedure_info['penalty_for_nonpayment'].get('punishment', 'N/A')}"

        prompt = f"""당신은 한국 근로기준법 전문 상담 AI입니다. 사용자의 질문에 실무적이고 정확한 답변을 제공합니다.

사용자 질문: {question}

참고할 법령 정보:
{law_context}{procedure_context}

답변 지침 (반드시 따를 것):

1. 필수 구성 (이 순서대로):
   - 공감 표현: 사용자의 상황을 인정하는 2~3문장 (따뜻하지만 짧게)
     예시: "그 상황이라면 정말 답답하고 힘드실 거 같습니다. 임금은 당연히 받아야 할 권리니까요. 다행히 법적으로 충분히 대응할 수 있습니다."
   - 관련 법적 근거: 어떤 법령의 어떤 조항인지 명시 (예: 근로기준법 제36조 제1항)
   - 절차 단계: "1단계 → 2단계 → 3단계" 순서대로, 각 단계마다:
     * 신청 기관/방법
     * 필요한 서류 (구체적)
     * 예상 처리 기간
   - 금액/비용: 구체적 한도나 계산식
   - 불이행 시 조치: 형사 처벌, 행정 제재 등

2. 금지사항 (절대 하지 말 것):
   - 과도한 감정 표현이나 반복되는 위로 금지 ("걱정하지 마세요" 같은 추가 격려 금지)
   - "화이팅", "파이팅", "힘내세요" 같은 격려 금지
   - 마크다운 문법(**볼드**, ###제목, ---, 번호 리스트) 사용 금지
   - 맥락에서 언급되지 않은 조항, 절차, 서류 절대 지어내기 금지

3. 확실하지 않은 정보:
   - 제공된 정보에 없으면 "이 부분은 관할 지방고용노동청(1350)에 확인이 필요합니다"라고 명시
   - 절대 추측이나 일반론으로 채우지 말 것

4. 표현 방식:
   - 자연스러운 문장으로 작성 (마크다운 금지)
   - 법률 용어는 정확하되, 일반인도 이해할 수 있게
   - 연락처는 구체적으로 (1350, law.go.kr, 지방고용노동청 등)
   - 간결하고 명확하게, 불필요한 설명 제외"""

        response = model.generate_content(prompt)
        base_answer = response.text

        # 수집일자 조회
        collection_date = get_collection_date()

        # 답변에 법령 최신 정보 고지 추가
        disclaimer = f"\n\n—\n본 답변은 {collection_date} 기준 근로기준법을 근거로 하며, 최신 정보는 국가법령정보센터(law.go.kr)에서 확인하실 수 있습니다."
        return base_answer + disclaimer

    except Exception as e:
        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
        collection_date = get_collection_date()
        disclaimer = f"\n\n—\n본 답변은 {collection_date} 기준 근로기준법을 근거로 하며, 최신 정보는 국가법령정보센터(law.go.kr)에서 확인하실 수 있습니다."
        return f"AI 상담 처리 중 오류가 발생했습니다: {str(e)}\n\n관련 법 근거:\n{context}{disclaimer}"


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """워크챗 (RAG + 절차 정보 + Gemini API)"""
    # Step 1: RAG로 관련 법조문 검색
    related_articles = search_labor_law_rag(req.question, top_k=5)

    # Step 2: 질문과 관련된 행정 절차 검색
    procedure_info = search_procedures(req.question)
    procedure_data = procedure_info[0] if procedure_info else None

    # Step 3: Gemini로 답변 생성 (법조문 + 절차 정보 함께 전달)
    answer = generate_answer(req.question, related_articles, procedure_data)

    # Step 4: 채팅 이력 저장
    chat_id = store.save_chat(0, req.question, answer)

    return ChatResponse(
        answer=answer,
        sources=[Source(law=a["law"], content=a["content"]) for a in related_articles],
        chat_id=chat_id,
    )


@router.get("/chat/history")
def get_chat_history(user_id: int = Depends(get_current_user_id)):
    return store.chat_history.get(user_id, [])
