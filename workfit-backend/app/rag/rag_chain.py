import os
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from app.rag.vector_store import vector_store_manager
from app.rag.documents import document_manager


class RAGChain:
    """근로기준법 RAG 체인"""

    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            self.enabled = False
            print("⚠️  ANTHROPIC_API_KEY 없음. RAG 비활성화됨")
            return

        self.enabled = True

        # Claude LLM 초기화
        self.llm = ChatAnthropic(
            api_key=api_key,
            model="claude-3-5-sonnet-20241022",
            temperature=0.7,
        )

        # VectorStore 초기화 및 문서 로드
        self._initialize_vector_store()

        # RAG 프롬프트 설정
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""다음은 근로기준법 관련 정보입니다.

문제: {question}

다음 정보를 바탕으로 답변해주세요:
{context}

답변:""",
        )

        # RAG 체인 초기화
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=vector_store_manager.get_vector_store().as_retriever(
                search_kwargs={"k": 3}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt},
        )

    def _initialize_vector_store(self):
        """VectorStore 초기화 및 문서 로드"""
        try:
            # 이미 문서가 있는지 확인
            vector_store = vector_store_manager.get_vector_store()

            # 컬렉션에 문서가 없으면 추가
            if vector_store._collection.count() == 0:
                print("📚 문서를 VectorStore에 추가 중...")
                texts, metadatas = document_manager.load_documents()
                vector_store_manager.add_documents(texts, metadatas)
                print(f"✅ {len(texts)}개 문서 청크 추가 완료")
            else:
                print("✅ VectorStore 준비 완료")
        except Exception as e:
            print(f"⚠️  VectorStore 초기화 중 오류: {e}")

    def query(self, question: str) -> dict:
        """RAG 쿼리 실행"""
        if not self.enabled:
            return {
                "answer": "API 키 설정이 필요합니다. .env 파일에 ANTHROPIC_API_KEY를 추가해주세요.",
                "sources": [],
                "success": False,
            }

        try:
            result = self.qa_chain.invoke({"query": question})

            return {
                "answer": result.get("result", "답변을 생성하지 못했습니다."),
                "sources": [
                    doc.metadata.get("topic", "알 수 없음")
                    for doc in result.get("source_documents", [])
                ],
                "success": True,
            }
        except Exception as e:
            print(f"❌ RAG 쿼리 오류: {e}")
            return {
                "answer": f"오류 발생: {str(e)}",
                "sources": [],
                "success": False,
            }


# 전역 RAG 체인 인스턴스
rag_chain = RAGChain()
