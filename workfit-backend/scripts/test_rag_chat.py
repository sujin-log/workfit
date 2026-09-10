"""
워크챗 RAG 파이프라인 실제 테스트
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import json

# .env 로드
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

# 테스트용 임시 환경변수 설정
if not os.getenv("GOOGLE_API_KEY"):
    print("[WARNING] GOOGLE_API_KEY가 설정되지 않았습니다")
    print("[INFO] 더미 답변 모드로 진행합니다\n")


def search_labor_law_rag(question: str, top_k: int = 5) -> list[dict]:
    """ChromaDB를 사용한 유사도 기반 근로기준법 검색"""
    import chromadb
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

    db_path = Path(__file__).parent.parent / "chroma_db"

    if not db_path.exists():
        print("[ERROR] ChromaDB를 찾을 수 없습니다")
        return []

    client = chromadb.PersistentClient(path=str(db_path))
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_collection(
        name="labor_law",
        embedding_function=embedding_function
    )

    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )

    articles = []
    if results and results['documents']:
        for doc, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        ):
            articles.append({
                "law": f"제{metadata.get('clause', '?')}조",
                "content": doc,
                "text": doc,
                "similarity": 1 - distance  # 유사도 점수
            })

    return articles


def generate_answer_gemini(question: str, related_articles: list[dict]) -> str:
    """Gemini API를 사용한 답변 생성"""
    import google.generativeai as genai

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        # API 키 없으면 간단한 답변
        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
        return f"(API 키 미설정) 관련 법 근거:\n{context}"

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-3.6-flash")

        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)

        prompt = f"""다음은 근로기준법 조항입니다:

{context}

사용자 질문: {question}

지침:
1. 위 법 조항을 근거로 친구처럼 편하게 답변해줘
2. 마크다운은 사용하지 마고 자연스러운 문장으로만 답변
3. 3~5문장 이내로 핵심만 짧게 답변
4. 카카오톡으로 친구가 설명해주는 듯한 편한 톤 유지"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        context = "\n".join(f"- {a['law']}: {a['content']}" for a in related_articles)
        return f"(오류 발생: {str(e)}) 관련 법 근거:\n{context}"


def test_chat(question: str):
    """채팅 테스트"""
    print("=" * 80)
    print(f"질문: {question}")
    print("=" * 80)

    # 1. ChromaDB 검색
    print("\n[STEP 1] ChromaDB에서 관련 조문 검색...")
    related_articles = search_labor_law_rag(question, top_k=5)

    print(f"검색 결과: {len(related_articles)}개 조문")
    for i, article in enumerate(related_articles, 1):
        print(f"\n  [{i}] {article['law']} (유사도: {article.get('similarity', 0):.2%})")
        print(f"      {article['content'][:80]}...")

    # 2. Gemini 답변 생성
    print("\n[STEP 2] Gemini API로 답변 생성...")
    answer = generate_answer_gemini(question, related_articles)

    print(f"\n답변:\n{answer}")
    print("\n" + "=" * 80 + "\n")

    return {
        "question": question,
        "related_articles": [
            {
                "law": a["law"],
                "content": a["content"],
                "similarity": a.get("similarity", 0)
            }
            for a in related_articles
        ],
        "answer": answer
    }


if __name__ == "__main__":
    # 테스트 질문들
    test_questions = [
        "퇴사 후 임금을 안 줬어요. 어떻게 해야 하나요?",
        "야간근로를 했는데 추가 임금을 안 줬어요",
        "근로계약서 없이 일했어도 되나요?",
    ]

    results = []

    print("\n")
    print("#" * 80)
    print("# 워크챗 RAG 파이프라인 실제 테스트")
    print("#" * 80)
    print("\n")

    for question in test_questions:
        result = test_chat(question)
        results.append(result)

    # 결과 저장
    output_file = Path(__file__).parent.parent / "test_results.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] 테스트 결과가 저장되었습니다: {output_file}")
