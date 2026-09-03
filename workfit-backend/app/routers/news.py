from fastapi import APIRouter, HTTPException
from app import store

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/trend")
def get_trend(keyword: str = "청년취업", days: int = 7):
    # TODO: 인증키 발급되면 여기를 실제 빅카인즈 time_line API 호출로 교체
    data = store.load_json("news_trend.json")
    return data


@router.get("/category-ratio")
def get_category_ratio():
    data = store.load_json("ratios.json")
    return data["category_ratio"]


@router.get("/sentiment-ratio")
def get_sentiment_ratio():
    data = store.load_json("ratios.json")
    return data["sentiment_ratio"]


@router.get("/list")
def get_news_list(category: str | None = None):
    news = store.load_json("news_list.json")
    if category:
        news = [n for n in news if category in n["category"]]
    return news


@router.get("/{news_id}")
def get_news_detail(news_id: str):
    news = store.load_json("news_list.json")
    for n in news:
        if n["news_id"] == news_id:
            return n
    raise HTTPException(status_code=404, detail="뉴스를 찾을 수 없습니다.")
