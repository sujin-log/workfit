import os
from pathlib import Path
from datetime import datetime
from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse, Source
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api", tags=["chat"])


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

        # 검색 결과를 Source 형식으로 변환
        articles = []
        if results and results['documents']:
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                articles.append({
                    "law": f"제{metadata.get('clause', '?')}조",
                    "content": doc,
                    "text": doc
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


def generate_answer(question: str, related_articles: list[dict]) -> str:
    """Google Gemini API를 사용한 답변 생성 (법령 최신 정보 고지 포함)"""
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
        return f"Google Gemini API 키가 설정되지 않았습니다.\n\n관련 법 근거:\n{context}"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.6-flash")

        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)

        prompt = f"""다음은 청년 정책 관련 법 조항입니다:

{context}

사용자 질문: {question}

지침:
1. 위 법 조항을 참고해서 친구처럼 편하게 답변해줘
2. 마크다운 문법(**볼드**, ###제목, ---, 번호 리스트 등)은 절대 쓰지 말고 자연스러운 문장으로만 답변
3. 3~5문장 이내로 핵심만 짧게 답변
4. 카카오톡으로 친구가 설명해주는 듯한 편한 톤 유지"""

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
    """워크챗 (RAG + Gemini API)"""
    # RAG로 관련 조문 검색
    related = search_labor_law_rag(req.question, top_k=5)

    # Gemini로 답변 생성
    answer = generate_answer(req.question, related)

    # 채팅 이력 저장
    chat_id = store.save_chat(0, req.question, answer)

    return ChatResponse(
        answer=answer,
        sources=[Source(law=a["law"], content=a["content"]) for a in related],
        chat_id=chat_id,
    )


@router.get("/chat/history")
def get_chat_history(user_id: int = Depends(get_current_user_id)):
    return store.chat_history.get(user_id, [])
