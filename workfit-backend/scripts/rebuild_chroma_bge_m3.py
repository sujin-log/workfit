"""
ChromaDB를 bge-m3 임베딩으로 재구축
성능 모니터링 포함
"""
import json
import time
import psutil
import os
from pathlib import Path
from datetime import datetime
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def get_memory_usage():
    """현재 메모리 사용량 반환"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def rebuild_chroma_with_bge_m3():
    """bge-m3로 ChromaDB 재구축 (수집일자 메타데이터 포함)"""
    print("=" * 80)
    print("ChromaDB 재구축 (bge-m3 임베딩)")
    print("=" * 80)

    start_time = time.time()
    initial_memory = get_memory_usage()

    # 수집일자 (ISO 8601 형식)
    collection_date = datetime.now().strftime("%Y-%m-%d")

    # 1. 조문 데이터 로드
    print("\n[STEP 1] 조문 데이터 로드...")
    json_file = Path(__file__).parent.parent / "mock_data" / "labor_articles.json"

    with open(json_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"  ✓ {len(articles)}개 조문 로드됨")

    # 2. ChromaDB 초기화
    print("\n[STEP 2] ChromaDB 초기화...")
    db_path = Path(__file__).parent.parent / "chroma_db_bge_m3"
    db_path.mkdir(exist_ok=True)

    client = chromadb.PersistentClient(path=str(db_path))

    # 기존 컬렉션 삭제
    try:
        client.delete_collection(name="labor_law")
        print("  ✓ 기존 컬렉션 삭제됨")
    except:
        pass

    # 3. bge-m3 임베딩 함수 로드
    print("\n[STEP 3] bge-m3 모델 로드...")
    model_load_start = time.time()

    embedding_function = SentenceTransformerEmbeddingFunction(
        model_name="BAAI/bge-m3"
    )

    model_load_time = time.time() - model_load_start
    current_memory = get_memory_usage()

    print(f"  ✓ bge-m3 로드 완료")
    print(f"    로드 시간: {model_load_time:.2f}초")
    print(f"    메모리 사용: {current_memory:.1f}MB (+{current_memory - initial_memory:.1f}MB)")

    # 4. 새 컬렉션 생성
    print("\n[STEP 4] 새 컬렉션 생성...")
    collection = client.create_collection(
        name="labor_law",
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_function
    )

    # 5. 조문 임베딩 및 저장
    print("\n[STEP 5] 조문 임베딩 및 저장...")
    embed_start = time.time()
    batch_size = 10

    for i in range(0, len(articles), batch_size):
        batch_articles = articles[i:i+batch_size]

        ids = []
        documents = []
        metadatas = []

        for article in batch_articles:
            unique_key = article.get('unique_key', article['clause'])
            doc_id = f"article_{unique_key}"
            ids.append(doc_id)
            documents.append(article['text'])
            metadatas.append({
                "clause": article['clause'],
                "title": article['title'],
                "type": "labor_law",
                "collection_date": collection_date
            })

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        current_memory = get_memory_usage()
        elapsed = time.time() - embed_start
        print(f"  [{min(i+batch_size, len(articles))}/{len(articles)}] " +
              f"시간: {elapsed:.1f}초 | 메모리: {current_memory:.1f}MB")

    embed_time = time.time() - embed_start
    final_memory = get_memory_usage()

    print(f"\n✓ 임베딩 완료")
    print(f"  총 임베딩 시간: {embed_time:.1f}초")
    print(f"  평균 시간/조문: {embed_time/len(articles)*1000:.1f}ms")
    print(f"  최종 메모리: {final_memory:.1f}MB")
    print(f"  메모리 증가: +{final_memory - initial_memory:.1f}MB")

    total_time = time.time() - start_time

    print(f"\n" + "=" * 80)
    print(f"재구축 완료!")
    print(f"  경로: {db_path}")
    print(f"  조문 수: {len(articles)}")
    print(f"  수집일자: {collection_date}")
    print(f"  총 소요 시간: {total_time:.1f}초")
    print(f"  모델: bge-m3 (BAAI/bge-m3)")
    print("=" * 80)

    return collection, articles


if __name__ == "__main__":
    print()
    rebuild_chroma_with_bge_m3()
