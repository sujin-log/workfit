"""
국가법령정보 공동활용 API (open.law.go.kr)
실제 근로기준법 데이터 수집
"""
import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# .env 로드
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)

# 정확한 API 엔드포인트 (open.law.go.kr 공식 가이드)
API_BASE = "https://open.law.go.kr"
API_KEY = os.getenv("LAW_API_OC")

print(f"\n[DEBUG] API_KEY: {API_KEY}")
print(f"[DEBUG] API_BASE: {API_BASE}\n")

if not API_KEY:
    print("[ERROR] LAW_API_OC 키가 .env에 설정되지 않았습니다")
    exit(1)


def find_labor_law_mst():
    """근로기준법의 법령 고유번호(MST) 찾기"""
    print("[STEP 1] 근로기준법 법령 고유번호(MST) 조회...")
    print("-" * 80)

    url = f"{API_BASE}/LSO/openApi/SearchLaw"
    params = {
        "OC": API_KEY,
        "lawNm": "근로기준법",
        "type": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.encoding = 'utf-8'

        print(f"[DEBUG] URL: {response.url}")
        print(f"[DEBUG] Status: {response.status_code}")

        if response.status_code != 200:
            print(f"[ERROR] API 호출 실패: {response.status_code}")
            print(f"[DEBUG] 응답: {response.text[:500]}")
            return None

        data = response.json()
        print(f"[DEBUG] 응답 구조: {list(data.keys())}")

        # 응답 구조 확인
        if "result" in data:
            result = data["result"]
            if isinstance(result, list) and len(result) > 0:
                law_info = result[0]
                mst = law_info.get("MST")
                law_nm = law_info.get("법령명")

                print(f"\n[OK] 근로기준법 발견!")
                print(f"    MST: {mst}")
                print(f"    법령명: {law_nm}")
                print(f"    시행일: {law_info.get('시행일')}")

                return mst

        print(f"[ERROR] 응답에서 근로기준법을 찾을 수 없습니다")
        print(f"[DEBUG] 전체 응답: {json.dumps(data, ensure_ascii=False, indent=2)[:1000]}")
        return None

    except Exception as e:
        print(f"[ERROR] 요청 실패: {e}")
        return None


def fetch_labor_law_articles(mst):
    """근로기준법 전체 조문 조회"""
    print("\n[STEP 2] 근로기준법 전체 조문 조회...")
    print("-" * 80)

    url = f"{API_BASE}/LSO/openApi/SearchLawInfo"
    params = {
        "OC": API_KEY,
        "MST": mst,
        "type": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.encoding = 'utf-8'

        print(f"[DEBUG] URL: {response.url}")
        print(f"[DEBUG] Status: {response.status_code}")

        if response.status_code != 200:
            print(f"[ERROR] API 호출 실패: {response.status_code}")
            print(f"[DEBUG] 응답: {response.text[:500]}")
            return None

        data = response.json()

        # 응답 구조 확인
        if isinstance(data, dict) and "articles" in data:
            articles = data["articles"]
            print(f"[OK] {len(articles)}개 조문 수집됨")
            return articles

        # 다른 응답 구조 시도
        if isinstance(data, list):
            print(f"[OK] {len(data)}개 조문 수집됨 (리스트 형식)")
            return data

        print(f"[WARNING] 예상치 못한 응답 구조")
        print(f"[DEBUG] 응답 타입: {type(data)}")
        print(f"[DEBUG] 응답 키: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
        print(f"[DEBUG] 첫 1000자: {json.dumps(data, ensure_ascii=False)[:1000]}")

        return data if isinstance(data, (list, dict)) else None

    except Exception as e:
        print(f"[ERROR] 요청 실패: {e}")
        return None


def parse_articles(raw_data):
    """조문 데이터 파싱"""
    print("\n[STEP 3] 조문 데이터 파싱...")
    print("-" * 80)

    articles = []

    if isinstance(raw_data, list):
        for item in raw_data:
            if isinstance(item, dict):
                # 조 번호와 내용 추출
                clause_num = item.get("조", item.get("clause", ""))
                content = item.get("조문내용", item.get("content", ""))

                if clause_num and content:
                    articles.append({
                        "clause": str(clause_num),
                        "content": content,
                        "text": f"제{clause_num}조\n{content}"
                    })

    elif isinstance(raw_data, dict):
        # dict 구조 처리
        for key, value in raw_data.items():
            if isinstance(value, dict):
                clause_num = value.get("조", value.get("clause", key))
                content = value.get("조문내용", value.get("content", ""))

                if content:
                    articles.append({
                        "clause": str(clause_num),
                        "content": content,
                        "text": f"제{clause_num}조\n{content}"
                    })

    print(f"[OK] {len(articles)}개 조문 파싱 완료")

    return articles


def save_articles(articles):
    """조문 데이터 저장"""
    print("\n[STEP 4] 조문 데이터 저장...")
    print("-" * 80)

    output_dir = Path(__file__).parent.parent / "mock_data"
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "labor_articles.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"[OK] {len(articles)}개 조문이 저장되었습니다")
    print(f"    경로: {output_file}")

    return articles


if __name__ == "__main__":
    print("=" * 80)
    print("근로기준법 실제 데이터 수집 (open.law.go.kr API)")
    print("=" * 80)
    print()

    # 1. MST 찾기
    mst = find_labor_law_mst()

    if not mst:
        print("\n[FATAL] MST를 찾을 수 없습니다. 작업 중단.")
        exit(1)

    # 2. 조문 데이터 조회
    raw_data = fetch_labor_law_articles(mst)

    if not raw_data:
        print("\n[FATAL] 조문 데이터를 가져올 수 없습니다. 작업 중단.")
        exit(1)

    # 3. 파싱
    articles = parse_articles(raw_data)

    if not articles:
        print("\n[FATAL] 파싱된 조문이 없습니다. 작업 중단.")
        print("[DEBUG] raw_data 전체:")
        print(json.dumps(raw_data, ensure_ascii=False, indent=2)[:2000])
        exit(1)

    # 4. 저장
    articles = save_articles(articles)

    # 5. 샘플 출력
    print("\n[STEP 5] 수집된 조문 샘플 (첫 5개)...")
    print("=" * 80)

    for i, article in enumerate(articles[:5], 1):
        print(f"\n[{i}] 제{article['clause']}조")
        print(f"    {article['content'][:100]}...")

    print("\n" + "=" * 80)
    print(f"[완료] 총 {len(articles)}개 조문 수집 완료!")
    print("=" * 80)
