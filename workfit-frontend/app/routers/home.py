from fastapi import APIRouter
from app import store

router = APIRouter(prefix="/api/home", tags=["home"])


@router.get("/summary")
def summary():
    news_trend = store.load_json("news_trend.json")
    ratios = store.load_json("ratios.json")
    policies = store.load_json("policies.json")
    posts = sorted(store.posts, key=lambda p: p["likes"], reverse=True)

    return {
        "news_trend": news_trend,
        "category_ratio": ratios["category_ratio"],
        "sentiment_ratio": ratios["sentiment_ratio"],
        "recommended_policies": policies[:2],
        "hot_posts": [{"id": p["id"], "title": p["title"]} for p in posts[:3]],
    }
