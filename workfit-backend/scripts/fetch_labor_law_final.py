"""
국가법령정보 DRF API (정확한 엔드포인트)
근로기준법 실제 데이터 수집
"""
import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# .env 로드
env_file = Path(__file__).parent.parent / ".env"
load_dotenv(env_file)

API_KEY = os.getenv("LAW_API_OC")

if not API_KEY:
    print("[ERROR] LAW_API_OC 키가 .env에 설정되지 않았습니다")
    exit(1)


def step1_find_labor_law_mst():
    """1단계: 근로기준법 MST 찾기"""
    print("=" * 80)
    print("[STEP 1] 근로기준법 법령일련번호(MST) 조회")
    print("=" * 80)

    url = "https://www.law.go.kr/DRF/lawSearch.do"
    params = {
        "OC": API_KEY,
        "target": "law",
        "type": "JSON",
        "query": "근로기준법"
    }

    print(f"\n[DEBUG] URL: {url}")
    print(f"[DEBUG] 파라미터: {params}\n")

    try:
        response = requests.get(url, params=params, timeout=15)
        response.encoding = 'utf-8'

        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Content-Type: {response.headers.get('content-type')}")
        print(f"[DEBUG] 응답 크기: {len(response.text)} bytes\n")

        # 먼저 원본 응답 출력
        print("[원본 응답 (처음 2000자)]")
        print("-" * 80)
        print(response.text[:2000])
        print("-" * 80)

        # JSON 파싱 시도
        try:
            data = response.json()
            print(f"\n[OK] JSON 파싱 성공")
            print(f"[DEBUG] 응답 구조: {type(data)}")

            if isinstance(data, dict):
                print(f"[DEBUG] 최상위 키: {list(data.keys())}")

            print(f"\n[전체 응답 구조]")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])

            # MST 추출
            mst = None

            if "LawSearch" in data and "law" in data["LawSearch"]:
                laws = data["LawSearch"]["law"]
                if isinstance(laws, list) and len(laws) > 0:
                    # 첫 번째가 근로기준법(법률)
                    mst = laws[0].get("법령일련번호")
                    law_name = laws[0].get("법령명한글")
                    law_type = laws[0].get("법령구분명")

                    print(f"\n[OK] MST 발견!")
                    print(f"    법령명: {law_name}")
                    print(f"    법령구분: {law_type}")
                    print(f"    MST(법령일련번호): {mst}")
                    print(f"    시행일자: {laws[0].get('시행일자')}")

                    return mst

            print(f"\n[ERROR] MST를 찾을 수 없습니다")
            return None

        except json.JSONDecodeError as e:
            print(f"\n[ERROR] JSON 파싱 실패: {e}")
            print(f"[응답 전문]")
            print(response.text)
            return None

    except Exception as e:
        print(f"[ERROR] 요청 실패: {e}")
        return None


def step2_fetch_labor_law(mst):
    """2단계: 근로기준법 본문 조회"""
    print("\n" + "=" * 80)
    print(f"[STEP 2] 근로기준법 본문 조회 (MST: {mst})")
    print("=" * 80)

    url = "https://www.law.go.kr/DRF/lawService.do"
    params = {
        "OC": API_KEY,
        "target": "law",
        "MST": mst,
        "type": "JSON"
    }

    print(f"\n[DEBUG] URL: {url}")
    print(f"[DEBUG] 파라미터: {params}\n")

    try:
        response = requests.get(url, params=params, timeout=15)
        response.encoding = 'utf-8'

        print(f"[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Content-Type: {response.headers.get('content-type')}")
        print(f"[DEBUG] 응답 크기: {len(response.text)} bytes\n")

        # 먼저 원본 응답 출력
        print("[원본 응답 (처음 3000자)]")
        print("-" * 80)
        print(response.text[:3000])
        print("-" * 80)

        # JSON 파싱 시도
        try:
            data = response.json()
            print(f"\n[OK] JSON 파싱 성공")
            print(f"[DEBUG] 응답 타입: {type(data)}")

            if isinstance(data, dict):
                print(f"[DEBUG] 최상위 키: {list(data.keys())}")

            # 전체 응답을 파일로 저장
            response_file = Path(__file__).parent.parent / "law_response_step2.json"
            with open(response_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"\n[OK] 전체 응답을 파일로 저장했습니다")
            print(f"    경로: {response_file}")
            print(f"    크기: {len(json.dumps(data, ensure_ascii=False))} bytes")

            # 최상위 키 목록
            if "법령" in data:
                law_data = data["법령"]
                print(f"\n[법령] 키 목록:")
                for key in list(law_data.keys())[:15]:
                    print(f"    - {key}")

                # 조문 찾기
                if "조문" in law_data:
                    print(f"\n[OK] '조문' 키 발견!")
                    articles = law_data["조문"]
                    print(f"    조문 개수: {len(articles) if isinstance(articles, list) else 'N/A'}")
                elif "조" in law_data:
                    print(f"\n[OK] '조' 키 발견!")
                elif "본문" in law_data:
                    print(f"\n[OK] '본문' 키 발견!")

            print(f"\n[응답 구조 (첫 3000자)]")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])

            return data

        except json.JSONDecodeError as e:
            print(f"\n[ERROR] JSON 파싱 실패: {e}")
            print(f"[응답 전문 (처음 5000자)]")
            print(response.text[:5000])
            return None

    except Exception as e:
        print(f"[ERROR] 요청 실패: {e}")
        return None


if __name__ == "__main__":
    print("\n")
    print("#" * 80)
    print("# 국가법령정보 DRF API - 근로기준법 데이터 수집")
    print("#" * 80)
    print()

    # 1단계: MST 찾기
    mst = step1_find_labor_law_mst()

    if not mst:
        print("\n[FATAL] MST를 찾을 수 없습니다. 작업 중단.")
        print("[대기중] 응답 구조를 분석한 후 파싱 코드를 수정하세요.")
        exit(1)

    # 2단계: 본문 조회
    data = step2_fetch_labor_law(mst)

    if not data:
        print("\n[FATAL] 근로기준법 본문을 가져올 수 없습니다. 작업 중단.")
        print("[대기중] 응답 구조를 분석한 후 파싱 코드를 수정하세요.")
        exit(1)

    print("\n" + "#" * 80)
    print("# [대기중] 응답 구조를 확인하고 파싱 코드를 작성하세요")
    print("#" * 80)
