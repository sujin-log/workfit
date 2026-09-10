"""
근로기준법 조문을 ChromaDB에 임베딩하여 저장
로컬 모델 사용 (OpenAI API 키 불필요)
"""
import json
import os
from pathlib import Path
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def load_labor_articles():
    """저장된 근로기준법 조문 로드"""
    json_file = Path(__file__).parent.parent / "mock_data" / "labor_articles.json"

    if not json_file.exists():
        print(f"[ERROR] 파일을 찾을 수 없습니다: {json_file}")
        return []

    with open(json_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"[OK] {len(articles)}개 조문을 로드했습니다")
    return articles


def build_chroma_db(articles):
    """ChromaDB 생성 및 임베딩 저장"""
    print("[INFO] ChromaDB 초기화 중...")

    # ChromaDB 경로 설정 (프로젝트 내 로컬 저장)
    db_path = Path(__file__).parent.parent / "chroma_db"
    db_path.mkdir(exist_ok=True)

    # ChromaDB 클라이언트 생성 (새로운 방식)
    client = chromadb.PersistentClient(path=str(db_path))

    # 기존 컬렉션 삭제 (재생성)
    try:
        client.delete_collection(name="labor_law")
        print("[INFO] 기존 컬렉션을 삭제했습니다")
    except:
        pass

    # 임베딩 함수 설정 (sentence-transformers)
    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # 새 컬렉션 생성
    collection = client.create_collection(
        name="labor_law",
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_function
    )

    # 조문 임베딩 저장
    print("[INFO] 조문을 임베딩하여 저장 중...")

    ids = []
    documents = []
    metadatas = []

    for i, article in enumerate(articles):
        doc_id = f"article_{article.get('clause', f'unknown_{i}')}"
        text = article.get("text", "")
        clause = article.get("clause", "unknown")

        if text:
            ids.append(doc_id)
            documents.append(text)
            metadatas.append({
                "clause": str(clause),
                "type": "labor_law"
            })

    # 배치 저장 (한 번에 여러 개 저장하면 효율적)
    batch_size = 10
    for i in range(0, len(ids), batch_size):
        batch_ids = ids[i:i+batch_size]
        batch_docs = documents[i:i+batch_size]
        batch_meta = metadatas[i:i+batch_size]

        collection.add(
            ids=batch_ids,
            documents=batch_docs,
            metadatas=batch_meta
        )
        print(f"[OK] {min(i+batch_size, len(ids))}/{len(ids)} 조문 저장됨")

    print(f"\n[OK] ChromaDB 생성 완료: {db_path}")
    print(f"[OK] 총 {len(ids)}개 조문이 저장되었습니다")

    return db_path


def test_search(articles):
    """검색 기능 테스트"""
    print("\n[INFO] 검색 기능 테스트 중...")

    db_path = Path(__file__).parent.parent / "chroma_db"

    # 새로운 방식으로 클라이언트 생성
    client = chromadb.PersistentClient(path=str(db_path))
    collection = client.get_collection(name="labor_law")

    # 테스트 질문
    test_queries = [
        "근로자의 정의가 뭐야?",
        "최소 임금은?",
        "주당 근로시간",
    ]

    for query in test_queries:
        print(f"\n[QUERY] {query}")
        results = collection.query(
            query_texts=[query],
            n_results=3
        )

        if results and results['documents']:
            for doc, distance in zip(results['documents'][0], results['distances'][0]):
                print(f"  - 유사도: {1-distance:.2f}")
                print(f"    {doc[:80]}...")
        else:
            print("  [NO RESULTS]")


if __name__ == "__main__":
    # 1. 조문 로드
    articles = load_labor_articles()

    if not articles:
        print("[ERROR] 조문을 로드할 수 없습니다")
        exit(1)

    # 2. ChromaDB 생성 및 임베딩 저장
    db_path = build_chroma_db(articles)

    # 3. 검색 테스트
    test_search(articles)

    print("\n[OK] RAG 데이터베이스 구축이 완료되었습니다!")
