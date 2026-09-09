import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from app.rag.embeddings import KoreanEmbeddings
from pathlib import Path


class VectorStoreManager:
    """Chroma VectorDB 관리"""

    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        Path(persist_directory).mkdir(parents=True, exist_ok=True)

        # 임베딩 모델 초기화
        self.embeddings = KoreanEmbeddings()

        # Chroma 클라이언트 초기화
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection_name = "labor_law"

    def get_vector_store(self) -> Chroma:
        """VectorStore 반환"""
        return Chroma(
            client=self.client,
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

    def add_documents(self, documents: list, metadatas: list = None):
        """문서 추가"""
        vector_store = self.get_vector_store()
        vector_store.add_texts(texts=documents, metadatas=metadatas)
        return True

    def search(self, query: str, k: int = 3) -> list:
        """유사한 문서 검색"""
        vector_store = self.get_vector_store()
        results = vector_store.similarity_search(query, k=k)
        return results

    def clear(self):
        """VectorDB 초기화"""
        self.client.delete_collection(name=self.collection_name)
        return True


# 전역 VectorStore 인스턴스
vector_store_manager = VectorStoreManager()
