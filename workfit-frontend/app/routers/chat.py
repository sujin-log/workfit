import os
from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse, Source
from app import store
from app.auth_utils import get_current_user_id

router = APIRouter(prefix="/api", tags=["chat"])


def search_related_articles(question: str, top_k: int = 2) -> list[dict]:
    """
    벡터DB 없이 키워드 겹침 개수로 관련 조항을 찾는 가장 단순한 방식.
    나중에 여유 있으면 sentence-transformers 임베딩 + 코사인 유사도로 업그레이드 가능.
    """
    articles = store.load_json("law_articles.json")
    scored = []
    for a in articles:
        score = sum(1 for kw in a["keywords"] if kw in question)
        if score > 0:
            scored.append((score, a))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [a for _, a in scored[:top_k]] or articles[:1]  # 매칭 없으면 기본 조항 1개라도 반환


def generate_answer(question: str, related_articles: list[dict]) -> str:
    """
    ANTHROPIC_API_KEY가 .env에 설정돼 있으면 실제 Claude API 호출,
    없으면 데모/개발용 canned 답변 반환 (오프라인에서도 화면 개발 가능하게).
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)

    if not api_key:
        return (
            f"[개발용 더미 답변] 질문: '{question}'\n\n"
            f"관련 법 근거:\n{context}\n\n"
            f"실제 배포 전 ANTHROPIC_API_KEY를 .env에 설정하면 이 자리에 Claude가 생성한 실제 답변이 표시됩니다."
        )

    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    prompt = (
        f"너는 청년 노무 상담 챗봇이야. 아래 법 조항 근거를 바탕으로 질문에 답변해줘.\n\n"
        f"[근거 조항]\n{context}\n\n[질문]\n{question}"
    )
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    # 워크챗은 비로그인 상태에서도 사용 가능하게 설계 (user_id=0은 '비회원'을 의미)
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
