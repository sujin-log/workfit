from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings
from typing import List


class KoreanEmbeddings(Embeddings):
    """한국어 특화 임베딩 모델 (bge-m3)"""

    def __init__(self, model_name: str = "BAAI/bge-m3"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """문서 텍스트 임베딩"""
        embeddings = self.model.encode(texts, convert_to_tensor=False)
        return [embedding.tolist() for embedding in embeddings]

    def embed_query(self, text: str) -> List[float]:
        """사용자 질문 임베딩"""
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()
