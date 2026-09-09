from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Tuple


# 샘플 근로기준법 내용 (실제로는 파일에서 로드)
LABOR_LAW_DOCUMENTS = {
    "최저임금": """
    [근로기준법 제6조]
    최저임금이란 사용자가 근로자에게 지급하여야 할 임금의 최저수준을 정하는 제도입니다.

    2024년 최저임금: 시간급 10,860원, 월급 2,290,660원
    - 적용 대상: 일반근로자, 시간제근로자 모두 적용
    - 예외: 공익법인, 사회적기업 등 별도 규정

    위반시 처벌: 3년 이하 징역 또는 2천만원 이하 벌금
    """,

    "휴가": """
    [근로기준법 제15조]
    근로자는 1년간 8일 이상의 유급휴가를 받을 권리가 있습니다.

    연차휴가 규정:
    - 입사 후 1년 경과: 15일 (1월 1일 기준)
    - 3년 이상: 3년마다 1일 추가 (최대 25일)
    - 사용하지 않은 휴가: 3년 경과시 소멸

    기타 휴가:
    - 국경일: 유급휴일
    - 생리휴가: 여성근로자 월 1일
    - 출산휴가: 여성근로자 90일 (산전 45일, 산후 45일)
    """,

    "해고": """
    [근로기준법 제23조]
    사용자가 근로자를 해고할 때는 다음을 지켜야 합니다.

    정당한 이유가 있는 경우:
    - 근로자의 책임있는 행동으로 인한 손해
    - 성실성 부족
    - 업무 능력 부족

    부당해고:
    - 정당한 이유 없는 해고는 무효
    - 30일 전 예고 필요
    - 예고하지 않을 경우 30일분 통상임금 지급 필요

    구제청구: 해고 후 3개월 이내 부당해고 구제 신청 가능
    """,

    "초과근무": """
    [근로기준법 제15조]
    근로시간은 주 40시간을 초과할 수 없습니다.

    기본 규정:
    - 기본 근로시간: 주 40시간
    - 1주 15시간 초과근무 가능
    - 월 120시간 초과근무 한도

    연장근로 임금:
    - 50% 이상 가산금 지급 (기본급 기준)
    - 예) 시간급 10,000원 → 15,000원 이상

    야간근로/휴일근로:
    - 야간(22시~06시): 50% 가산금
    - 휴일: 50% 가산금
    """,
}


class DocumentManager:
    """근로기준법 문서 관리"""

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", " ", ""],
        )

    def load_documents(self) -> Tuple[List[str], List[dict]]:
        """모든 문서 로드 및 청킹"""
        all_texts = []
        all_metadatas = []

        for topic, content in LABOR_LAW_DOCUMENTS.items():
            # 문서 청킹
            chunks = self.text_splitter.split_text(content)

            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_metadatas.append({
                    "topic": topic,
                    "chunk_index": i,
                    "source": "근로기준법",
                })

        return all_texts, all_metadatas

    def get_sample_query(self) -> List[str]:
        """샘플 질문"""
        return [
            "최저임금이 뭐예요?",
            "연차휴가는 몇 일이에요?",
            "해고당했는데 부당해고인가요?",
            "초과근무 수당은 어떻게 되나요?",
        ]


# 전역 DocumentManager 인스턴스
document_manager = DocumentManager()
