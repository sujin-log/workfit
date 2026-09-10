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
    """Google Gemini API를 사용한 답변 생성"""
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
        return response.text
    except Exception as e:
        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
        return f"AI 상담 처리 중 오류가 발생했습니다: {str(e)}\n\n관련 법 근거:\n{context}"


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
