import os
from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse, Source
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api", tags=["chat"])


def search_related_articles(question: str, top_k: int = 2) -> list[dict]:
    """키워드 기반 조항 검색"""
    articles = store.load_json("law_articles.json")
    scored = []
    for a in articles:
        score = sum(1 for kw in a["keywords"] if kw in question)
        if score > 0:
            scored.append((score, a))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for _, a in scored[:top_k]] or articles[:1]


def generate_answer(question: str, related_articles: list[dict]) -> str:
    """더미 답변 생성 (RAG는 나중)"""
    context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
    return (
        f"[개발 중] 질문: '{question}'\n\n"
        f"관련 법 근거:\n{context}\n\n"
        f"실제 AI 상담은 후에 구현될 예정입니다."
    )


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """워크챗 (현재 더미 답변)"""
    related = search_related_articles(req.question)
    answer = generate_answer(req.question, related)
    chat_id = store.save_chat(0, req.question, answer)

    return ChatResponse(
        answer=answer,
        sources=[Source(law=a["law"], content=a["content"]) for a in related],
        chat_id=chat_id,
    )


@router.get("/chat/history")
def get_chat_history(user_id: int = Depends(get_current_user_id)):
    return store.chat_history.get(user_id, [])
